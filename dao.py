from models import Curso, Usuario

SQL_DELETA_CURSO = 'delete from curso where id = %s'
SQL_CURSO_POR_ID = 'SELECT id, nome, categoria, duracao from curso where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_CURSO = 'UPDATE curso SET nome=%s, categoria=%s, duracao=%s where id = %s'
SQL_BUSCA_CURSOS = 'SELECT id, nome, categoria, duracao from curso'
SQL_CRIA_CURSO = 'INSERT into curso (nome, categoria, duracao) values (%s, %s, %s)'


class CursoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, curso):
        cursor = self.__db.connection.cursor()

        if (curso.id):
            cursor.execute(SQL_ATUALIZA_CURSO, (curso.nome, curso.categoria, curso.duracao, curso.id))
        else:
            cursor.execute(SQL_CRIA_CURSO, (curso.nome, curso.categoria, curso.duracao))
            curso.id = cursor.lastrowid
        self.__db.connection.commit()
        return curso

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_CURSOS)
        cursos = traduz_cursos(cursor.fetchall())
        return cursos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CURSO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Curso(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_CURSO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_cursos(cursos):
    def cria_curso_com_tupla(tupla):
        return Curso(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_curso_com_tupla, cursos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
