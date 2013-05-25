drop index if exists AreaCode_1;
drop index if exists AreaCode_2;
drop index if exists NetCode_1;
drop index if exists NetCode_2;
drop table if exists AreaCode;
drop table if exists NetCode;
create table AreaCode (
    local_government_code text, 
    old_zipcode text,
    zipcode text,
    prefecture_kana text,
    municipality_kana text,
    street_kana text,
    prefecture_kanji text,
    municipality_kanji text,
    street_kanji text,
    street_has_plural_code text,
    street_has_code_by_section text,
    has_chome text,
    zipcode_shared_by_plural_street text,
    is_modified text,
    reason_of_modify text
);
create table NetCode (
    local_government_code text, 
    old_zipcode text,
    zipcode text,
    prefecture_kana text,
    municipality_kana text,
    street_kana text,
    prefecture_kanji text,
    municipality_kanji text,
    street_kanji text,
    street_has_plural_code text,
    street_has_code_by_section text,
    has_chome text,
    zipcode_shared_by_plural_street text,
    is_modified text,
    reason_of_modify text
);
create index AreaCode_1 on AreaCode (
    zipcode
);
create index AreaCode_2 on AreaCode (
    prefecture_kanji,
    municipality_kanji,
    street_kanji
);
create index NetCode_1 on NetCode (
    zipcode
);
create index NetCode_2 on NetCode (
    prefecture_kanji,
    municipality_kanji,
    street_kanji
);
.separator ","
.import ../db/area.csv AreaCode
.import ../db/net.csv NetCode
