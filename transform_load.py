import pandas as pd
import numpy as np
import re


class Load():
    def load_from_csv(self, path):
        return pd.read_csv(path)


class Transform:
    def merge_data(self, paths):
        dfs = [pd.read_csv(path) for path in paths]

        allowed_cols = ['score', 'economy', 'family', 'health',
                        'freedom', 'trust', 'generosity', 'dystopia']
        colums_dfs = [list(filter(lambda col: col != None,
                                  list(map(lambda col: col
                                           if self.firt_word(col).lower() in allowed_cols
                                           else None, df.columns))
                                  )) for df in dfs]

        dfs = [df.rename(columns=new_names) for df, new_names in list(
            zip(dfs, list(map(lambda colums_df: dict(zip(colums_df, allowed_cols)),
                              colums_dfs
                              ))))
               ]

        df_merged = dfs[0].loc[:, allowed_cols]

        for i in range(1, len(dfs)):
            df_merged = df_merged.append(dfs[i].loc[:, allowed_cols])

        df_merged = df_merged[allowed_cols].astype(float)
        df_merged = df_merged.dropna()
        print(df_merged.head())
        df_merged[allowed_cols].to_csv('./out/merged.csv', columns=allowed_cols, index=False)

    def firt_word(self, sense):
        return re.findall(r'\w+', sense)[0]


if __name__ == '__main__':
    transformer = Transform()
    transformer.merge_data(['./in/2015.csv',
                           './in/2016.csv',
                            './in/2017.csv',
                            ])
