DROP FUNCTION IF EXISTS pb_search(TEXT);
DROP FUNCTION IF EXISTS pb_get_page(INT, INT);

CREATE FUNCTION pb_search(search_text TEXT)
RETURNS TABLE(contact_id INT, contact_name TEXT, contact_phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.person_name, c.phone
    FROM pb_contacts c
    WHERE c.person_name ILIKE '%' || search_text || '%'
       OR c.phone ILIKE '%' || search_text || '%';
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION pb_get_page(lim INT, off INT)
RETURNS TABLE(contact_id INT, contact_name TEXT, contact_phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.person_name, c.phone
    FROM pb_contacts c
    ORDER BY c.id
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;