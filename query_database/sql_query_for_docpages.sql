-- name: head
-- Get the first five rows in the database
select *
from covid19_muckrock.docpages C
limit 5;

-- name: get_doc_titles
-- Get all document titles
select C.title
from covid19_muckrock.docpages C; 