document.addEventListener('DOMContentLoaded', function(e){
    renderAccordionsForMobile()
    renderHowSelector()
})

function renderAccordionsForMobile () {
    let accordions = document.getElementsByClassName('point__title')
    
    for (let i = 0; i < accordions.length; i++) {
        accordions[i].addEventListener('click', function () {
            this.classList.toggle('active')
            let panel = this.nextElementSibling
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null
            } else {
                panel.style.maxHeight = panel.scrollHeight + 'px'
            }
        })
    }
}

function renderHowSelector () {
    let howSelectors = document.getElementsByClassName('selector__element')
    let howSections = document.getElementsByClassName('sections__section')
    
    for (let i = 0; i < howSelectors.length; i++) {
        howSelectors[i].addEventListener('click', function () {
            for (let j = 0; j < howSelectors.length; j++) {
                howSelectors[j].classList.toggle('selector__element-selected')
                howSections[j].classList.toggle('sections__section-selected')
            }
        })
    }
}