const btnCadastrar = document.getElementById('btn-cadastrar');
const btnFechar = document.getElementById('btn-fechar');
const modalCadastrar = document.getElementById('modal-cadastrar');

btnCadastrar.addEventListener('click', () => {
modalCadastrar.style.display = 'block';
});

btnFechar.addEventListener('click', () => {
modalCadastrar.style.display = 'none';
});

const formCadastrar = document.querySelector('form');

formCadastrar.addEventListener('submit', (event) => {
event.preventDefault();
modalCadastrar.style.display = 'none';
});