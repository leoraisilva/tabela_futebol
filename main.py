from src.RequestTable import RequestTable


def print_hi():

    table = RequestTable()
    content = table.tabela("https://ge.globo.com/futebol/brasileirao-serie-a/")
    return content

if __name__ == '__main__':
    print(print_hi())

