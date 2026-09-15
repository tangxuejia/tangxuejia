-- KOS V0.23 content fix and validation contract.
-- The public client only calls public.kos_check_case_variant; answer keys stay private.

update public.kos_case_variants
set payload = jsonb_set(
  payload,
  '{interaction,options}',
  '[{"label":"8元","value":"8"},{"label":"12元","value":"12"},{"label":"27.5元","value":"27.5"}]'::jsonb
), updated_at = now()
where case_id = '001' and level = 1 and status = 'published';

update kos_validation_private.variant_answer_keys k
set rule = jsonb_set(
  jsonb_set(
    k.rule,
    '{solutionMode}',
    to_jsonb(coalesce(v.payload->>'solutionMode', case when v.case_id = '011' then 'multiple_valid' else 'set' end))
  ),
  '{feasible}',
  coalesce(k.rule->'answer', '[]'::jsonb)
)
from public.kos_case_variants v
where v.case_id = k.case_id
  and v.level = k.level
  and v.status = 'published'
  and (v.payload->'interaction'->>'type') = 'plan'
  and not (k.rule ? 'answers');

-- A plan's first-stage feasible set is part of the server decision. For alternative
-- sets, the selected final set must equal the first-stage set and match one answer key.
create or replace function kos_validation_private.check_case_variant(
  p_case_id text,
  p_level smallint,
  p_response jsonb
) returns jsonb
language plpgsql
security definer
set search_path to 'pg_catalog', 'public', 'kos_validation_private', 'pg_temp'
as $function$
declare
  r jsonb;
  typ text;
  mode text;
  ok boolean := false;
  feasible_ok boolean := true;
  tol numeric := 0;
  got_num numeric;
  exp_num numeric;
  got_arr jsonb;
  exp_arr jsonb;
  feasible_arr jsonb;
  reason_text text;
  min_reason int := 0;
  candidate jsonb;
  engine jsonb;
  choice_count int := 0;
begin
  select rule into r from kos_validation_private.variant_answer_keys
  where case_id = p_case_id and level = p_level;
  if r is null then
    return jsonb_build_object('passed',false,'code','NO_RULE','feedback','这个版本的判定规则还没有准备好。');
  end if;
  typ := coalesce(r->>'type','');
  mode := coalesce(r->>'solutionMode','');
  min_reason := coalesce(nullif(r->>'minReasonLength','')::int,6);

  -- Every plan response must carry the first-stage feasible set. The final
  -- choices may only come from that set, and all values must be published
  -- options. This check also applies before the special 027/030 evaluators.
  if typ = 'plan' then
    feasible_arr := coalesce(p_response->'feasible','[]'::jsonb);
    got_arr := coalesce(p_response->'choices','[]'::jsonb);
    if jsonb_typeof(feasible_arr) <> 'array'
       or jsonb_typeof(got_arr) <> 'array'
       or jsonb_array_length(feasible_arr) = 0
       or jsonb_array_length(got_arr) = 0
       or not (feasible_arr @> got_arr)
       or exists (
         select 1
         from jsonb_array_elements(feasible_arr) f
         where not exists (
           select 1
           from jsonb_array_elements(coalesce(r->'options','[]'::jsonb)) o
           where o->>'value' = f#>>'{}'
         )
       ) then
      return jsonb_build_object('passed',false,'validator','server','type','plan','feedback','先完成可行性筛选，并且最终选择只能来自已保留的方案。');
    end if;
  end if;

  if p_case_id = '020' then
    select public.kos_case020_question_value(coalesce(array(select jsonb_array_elements_text(coalesce(p_response,'[]'::jsonb))),array[]::text[])) into engine;
    return engine || jsonb_build_object('passed',coalesce((engine->>'valid')::boolean,false) and coalesce((engine->>'score')::int,0)>=60,'validator','server');
  elsif p_case_id = '024' and p_level >= 3 then
    select public.kos_case024_machine_check(coalesce(array(select jsonb_array_elements_text(coalesce(p_response,'[]'::jsonb))),array[]::text[])) into engine;
    return engine || jsonb_build_object('passed',coalesce((engine->>'testsPassed')::int,0)>=5,'validator','server');
  elsif p_case_id = '027' and typ = 'plan' then
    select count(distinct value) into choice_count
    from jsonb_array_elements_text(coalesce(p_response->'choices','[]'::jsonb)) value;
    select public.kos_case027_budget_evaluate(
      coalesce(array(select jsonb_array_elements_text(coalesce(p_response->'choices','[]'::jsonb))),array[]::text[]),
      coalesce(p_response->>'reason','')
    ) into engine;
    return engine || jsonb_build_object(
      'passed',
      coalesce((engine->>'valid')::boolean,false)
      or (coalesce((engine->>'budgetUsed')::numeric,101)<=100
          and coalesce((engine->>'hardConstraintMet')::boolean,false)
          and choice_count>=2
          and char_length(trim(coalesce(p_response->>'reason','')))>=min_reason),
      'validator','server');
  elsif p_case_id = '030' and p_level >= 3 and typ = 'plan' then
    select public.kos_case030_root_chain_evaluate(
      coalesce(array(select jsonb_array_elements_text(coalesce(p_response->'choices','[]'::jsonb))),array[]::text[]),
      coalesce(p_response->>'reason','')
    ) into engine;
    return engine || jsonb_build_object(
      'passed',
      coalesce((engine->>'valid')::boolean,false)
      or (coalesce((engine->>'systemInterventions')::int,0)>=2
          and coalesce((engine->>'pathsBlocked')::int,0)>=4
          and char_length(trim(coalesce(p_response->>'reason','')))>=min_reason),
      'validator','server');
  end if;

  if typ in ('single','time') then
    ok := coalesce(p_response #>> '{}','') = coalesce(r->>'answer','');
  elsif typ = 'number' then
    begin got_num := (p_response #>> '{}')::numeric; exception when others then got_num := null; end;
    begin exp_num := (r->>'answer')::numeric; exception when others then exp_num := null; end;
    tol := coalesce(nullif(r->>'tolerance','')::numeric,0);
    ok := got_num is not null and exp_num is not null and abs(got_num-exp_num) <= tol;
  elsif typ = 'multi' then
    got_arr := coalesce(p_response,'[]'::jsonb);
    exp_arr := coalesce(r->'answer','[]'::jsonb);
    ok := jsonb_typeof(got_arr)='array' and got_arr @> exp_arr and exp_arr @> got_arr;
  elsif typ = 'plan' then
    got_arr := coalesce(p_response->'choices','[]'::jsonb);
    feasible_arr := coalesce(p_response->'feasible','[]'::jsonb);
    reason_text := trim(coalesce(p_response->>'reason',''));
    if mode = 'alternative_sets' then
      feasible_ok := jsonb_typeof(feasible_arr)='array' and feasible_arr @> got_arr and got_arr @> feasible_arr;
    else
      exp_arr := coalesce(r->'feasible', r->'answer', '[]'::jsonb);
      feasible_ok := jsonb_typeof(feasible_arr)='array' and feasible_arr @> exp_arr and exp_arr @> feasible_arr;
    end if;
    if char_length(reason_text) >= min_reason and feasible_ok and jsonb_typeof(got_arr)='array' then
      if mode = 'multiple_valid' then
        exp_arr := coalesce(r->'answer','[]'::jsonb);
        ok := jsonb_array_length(got_arr)=1 and exp_arr @> got_arr;
      elsif r ? 'answers' then
        for candidate in select value from jsonb_array_elements(r->'answers') loop
          if got_arr @> candidate and candidate @> got_arr then ok := true; exit; end if;
        end loop;
      else
        exp_arr := coalesce(r->'answer','[]'::jsonb);
        ok := got_arr @> exp_arr and exp_arr @> got_arr;
      end if;
    end if;
  end if;

  return jsonb_build_object(
    'passed',ok,
    'validator','server',
    'type',typ,
    'feedback',case when ok then '方案通过服务器判定。' when typ='plan' and char_length(coalesce(reason_text,''))<min_reason then '方案还缺少足够的理由与取舍说明。' else '还没通过。请重新检查证据、条件和约束。' end
  );
end
$function$;

-- Consistency audit: this result must be empty for published single/multi/plan rows.
with variants as (
  select case_id, level, payload->'interaction' as i
  from public.kos_case_variants
  where status = 'published'
), issues as (
  select case_id, level, 'single-answer-not-in-options' as issue
  from variants v
  where i->>'type' = 'single'
    and not exists (select 1 from jsonb_array_elements(coalesce(i->'options','[]'::jsonb)) o where o->>'value' = i->>'answer')
  union all
  select case_id, level, 'multi-answer-not-in-options'
  from variants v
  where i->>'type' = 'multi'
    and exists (select 1 from jsonb_array_elements(coalesce(i->'answer','[]'::jsonb)) a where not exists (select 1 from jsonb_array_elements(coalesce(i->'options','[]'::jsonb)) o where o->>'value' = a#>>'{}'))
)
select * from issues order by case_id, level;
