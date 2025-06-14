document.getElementById('enviarBtn').addEventListener('click', function () {
    window.location.href = 'page2.html';
  });
  document.getElementById('voltarBtn').addEventListener('click', function () {
  window.location.href = 'index.html';
});
function validarCPF(cpf) {
  cpf = cpf.replace(/[^\d]+/g, '');
  if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

  let soma = 0;
  for (let i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
  let resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf.charAt(9))) return false;

  soma = 0;
  for (let i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf.charAt(10))) return false;

  return true;
}

document.getElementById("cadastroForm").addEventListener("submit", function (e) {
  const cpf = document.getElementById("cpf").value;
  if (!validarCPF(cpf)) {
    e.preventDefault();
    alert("CPF inválido. Por favor, insira um CPF válido.");
  }
});
