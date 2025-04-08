// Funkce pro inicializaci šipky v navbaru
function initializeArrowRotation() {
  const logoText = document.querySelector('.logo-text');
  const logoSVG = logoText ? logoText.nextElementSibling : null;
  const navbar = document.querySelector('.navbar');

  if (logoSVG) {
      // Inicializace pro rozbalení navbaru
      navbar.addEventListener('mouseenter', () => {
          if (navbar.classList.contains('expanded')) {
              logoSVG.style.transform = 'rotate(-180deg)';
          }
      });

      // Inicializace pro sbalení navbaru
      navbar.addEventListener('mouseleave', () => {
          logoSVG.style.transform = 'rotate(0deg)';
      });

      // Aktualizace při změně velikosti navbaru
      navbar.addEventListener('transitionend', () => {
          if (navbar.offsetWidth > 100) {
              logoSVG.style.transform = 'rotate(-180deg)';
              logoSVG.style.color = '#47a24a'; // Zelená barva při rozbalení
          } else {
              logoSVG.style.transform = 'rotate(0deg)';
              logoSVG.style.color = ''; // Původní barva při sbalení
          }
      });
  }
}

// Spuštění inicializace šipky po načtení stránky
document.addEventListener('DOMContentLoaded', initializeArrowRotation);
