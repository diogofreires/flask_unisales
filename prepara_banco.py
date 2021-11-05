import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='u563882891_diogo', passwd='bEUQL7@N&3|',
                       host='sql172.main-hosting.eu', port=3306)

# Descomente se quiser desfazer o banco...
conn.cursor().execute("DROP DATABASE IF EXISTS `u563882891_unisales`;")
conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `u563882891_unisales` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `u563882891_unisales`;
    CREATE TABLE `curso` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(80) COLLATE utf8_bin NOT NULL,
      `categoria` varchar(40) COLLATE utf8_bin NOT NULL,
      `duracao` varchar(10) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
    'INSERT INTO u563882891_unisales.usuario (id, nome, senha) VALUES (%s, %s, %s)',
    [
        ('diogo', 'Diogo Freires', 'flask'),
        ('fulano', 'Fulano De Tal', '1234'),
        ('teste', 'Usuario Teste', '4321')
    ])

cursor.execute('select * from u563882891_unisales.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo cursos
cursor.executemany(
    'INSERT INTO u563882891_unisales.curso (nome, categoria, duracao) VALUES (%s, %s, %s)',
    [
        ('Sistemas da Informacao', 'Tecnologia', '4 Anos'),
        ('Tecnologia em Analise e Desenvolvimento de Sistemas',
         'Tecnologia', '2,5 Anos'),
        ('Enfermagem', 'Saude', '5 Anos'),
        ('Farmacia', 'Saude', '5 Anos'),
        ('Engenharia Civil', 'Engenharias', '5 Anos'),
        ('Engenharia de Producao', 'Engenharias', '5 Anos'),
    ])

cursor.execute('select * from u563882891_unisales.curso')
print(' -------------  cursos:  -------------')
for curso in cursor.fetchall():
    print(curso[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()
