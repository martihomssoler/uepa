document.addEventListener('DOMContentLoaded', function(evemt){
    let accordions = document.getElementsByClassName('point__title')
    
    for (let i = 0; i < accordions.length; i++) {
        accordions[i].addEventListener('click', function () {
            this.classList.toggle('active')
            let panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + 'px';
            }
        })
    }
})