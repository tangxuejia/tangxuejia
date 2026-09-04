-- Keep the private validator key aligned with public.kos_case_variants.
update kos_validation_private.variant_answer_keys
set rule = jsonb_set(rule, '{answer}', '"27.5"'::jsonb)
where case_id = '001' and level = 1;

-- Expected result: zero rows.
with v as (
  select case_id, level, payload->'interaction' as i
  from public.kos_case_variants
  where status = 'published'
)
select case_id, level, i->>'type' as type, i->>'answer' as answer
from v
where i->>'type' = 'single'
  and not exists (
    select 1
    from jsonb_array_elements(coalesce(i->'options','[]'::jsonb)) o
    where o->>'value' = i->>'answer'
  )
order by case_id, level;
