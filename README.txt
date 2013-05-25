ZipCode                                                                                                                     
=======                                                                                                                     


日本の郵便番号と住所を相互に問合せます。

- 郵便番号から住所                                                                                                        
- 住所(都道府県、市区町村、町名)から郵便番号


使い方                                                                                                                       
------                                                                                                                       
                                                                                                                            
1. 住所から郵便番号
    http://your.own.site/adr2zip?pref=(都道府県)&muni=(市区町村)&street=(町名)         

2. 郵便番号から住所
    http://your.own.site/zip2adr?code=(郵便番号)


問合せ結果
----------

問合せ結果は、JSON形式で返します。
各項目については、下記のサイトの説明を参照してください。
    http://www.post.japanpost.jp/zipcode/dl/readme.html

似たような住所が複数見つかった場合は、当てはまるものをすべて返します。

