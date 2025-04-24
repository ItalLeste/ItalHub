from flask import session, abort

def controlar_acesso(perfis_permitidos:list):
    """
    Decorador de controle de acesso para determinados perfis.

    Exemplo:
        @app.route('/admin)
        @controlar_acesso(['admin'])
        def admin():
            return 'Página de admin.'
    """
    def verificar_permissao(funcao):
        def wrapper(*args, **kwargs):
            perfil_logado = session.get('perfil')
            print(f"Perfil logado: {perfil_logado}")
            if perfil_logado not in perfis_permitidos:
                abort(403)
            else:
                print(f'Usuário com perfil {perfil_logado} tem acesso.')
            return funcao(*args, **kwargs)
        return wrapper
    return verificar_permissao


if __name__ == "__main__":
    # Teste a função decoradora
    @controlar_acesso(['admin'])
    def admin():
        return 'Página de admin.'

    admin()