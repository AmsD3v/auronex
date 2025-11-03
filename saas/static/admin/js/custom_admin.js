// Destacar campo Extra bots ao carregar página
document.addEventListener('DOMContentLoaded', function() {
    const extraBotsField = document.getElementById('id_extra_bots');
    if (extraBotsField) {
        // Scroll suave até o campo ao carregar
        setTimeout(function() {
            extraBotsField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Piscar borda
            let count = 0;
            const interval = setInterval(function() {
                if (count < 6) {
                    extraBotsField.style.borderColor = count % 2 === 0 ? '#ff0000' : '#4CAF50';
                    count++;
                } else {
                    clearInterval(interval);
                    extraBotsField.style.borderColor = '#4CAF50';
                }
            }, 300);
        }, 1000);
    }
});



