from abc import ABC


class AbcCellUtils(object):

    @staticmethod
    def name_to_ind(name: str) -> tuple[int, int, str]:

        """ Преобразование имени ячейки форрмата A1 в индексы ячейки (1, 1)
        testing:

        >>>from itertools import chain
        >>>
        >>>base = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        >>>base2 = [i + j for i in base for j in base]
        >>>base3 = [i + j + i1 for i in base for j in base for i1 in base]
        >>>for ind, i in enumerate(base + base2 + base3, 1):
        >>>    print(ind, i, CellTools.name_to_ind(str(i)))
        >>>    assert ind == CellTools.name_to_ind(str(i)[1])

        :param name:
        :return: первый элемент - индекс по строке (тот, который циферками обозначается в таблице)
            Второй элемент - индекс по столбцу (порядковый номер буквы, начиная с единицы)
            Третий элемент - Буква (набор букв) ячейки
        """

        row_index = 1
        col_index: list[int] = []
        _chars = ""

        for ind, char in enumerate(name):
            print(char, char.isdigit())
            if char.isdigit():
                row_index = int(name[ind:])
                _chars = name[:ind - 1]
                break
            col_index.append(ord(char) - 64)
        col_index.reverse()
        print(col_index)
        col_index: int = sum([i * ((ord("Z") - ord("A") + 1) ** ind) for ind, i in enumerate(col_index)])
        return (row_index,  # Номер по столбцу. Аналогичен первому индексу в двумерном массиве
                col_index,  # Номер по строке. Аналогичен второму индексу в двумерном массиве
                _chars)

    @staticmethod
    def ind_to_name(col_index: int) -> str:
        """Функция получения буквы ячейки по порядковому номеру столбца

        testing:
        >>>from itertools import chain
        >>>
        >>>base = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        >>>base2 = [i + j for i in base for j in base]
        >>>base3 = [i + j + i1 for i in base for j in base for i1 in base]
        >>>for ind, i in enumerate(base + base2 + base3, 1):
        >>>    print(ind, i, CellTools.ind_to_name(ind))
        >>>    assert i == CellTools.ind_to_name(ind)

        :param col_index: номер ячейки, начиная с единицы. Если ячейка A124, то number=1
        :return: буквенный номер ячейки. Если number=4, то return "D"
        """

        res = []
        while True:
            d, m = divmod(col_index, 26)
            if m == 0:
                m = 26
                d -= 1
            res.append(m + 64)
            if d > 26:
                col_index = d
            elif 0 < d:  # 0 < d <= 26
                res.append(d + 64)
                break
            else:
                break
        res.reverse()
        return "".join([chr(i) for i in res])



