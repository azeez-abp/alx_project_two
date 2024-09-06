function changeDimensionNew() {
    let down = false;
    let body = document.querySelector(".body");
    let sideBar = document.querySelector(".side");
    let startX, sidebarStartWidth;

    function downEvent(ev) {
        if (ev.target.classList.contains('mover')) {
            down = true;
            startX = ev.clientX || ev.touches[0].clientX; // Use clientX for mouse or touches[0].clientX for touch
            sidebarStartWidth = parseFloat(sideBar.getBoundingClientRect().width);
        }
    }

    document.addEventListener('mousedown', (ev) => {
        downEvent(ev);
    });

    document.addEventListener('touchstart', (ev) => {
        downEvent(ev);
    });

    function moveEvent(ev) {
        ev.preventDefault(); // Prevent default action for both touch and mouse events
        if (down) {
            let clientX = ev.clientX || ev.touches[0].clientX; // Use clientX for mouse or touches[0].clientX for touch
            let deltaPosition = clientX - startX;
            let newSidebarWidth = sidebarStartWidth + deltaPosition;
            let newBodyWidth = window.innerWidth - newSidebarWidth;

            // Ensure widths are within limits
            if (newSidebarWidth >= 0 && newSidebarWidth <= window.innerWidth && newBodyWidth >= 0 && newBodyWidth <= window.innerWidth) {
                let sidebarPercentWidth = (newSidebarWidth / window.innerWidth) * 100;
                let bodyPercentWidth = (newBodyWidth / window.innerWidth) * 100;

                sideBar.style.width = sidebarPercentWidth + "%";
                body.style.width = bodyPercentWidth + "%";
            }
        }
    }

    document.addEventListener('mousemove', (ev) => {
        moveEvent(ev);
    });

    document.addEventListener('touchmove', (ev) => {
        moveEvent(ev);
    });

    function upEvent() {
        down = false;
    }

    document.addEventListener('mouseup', () => {
        upEvent();
    });

    document.addEventListener('touchend', () => {
        upEvent();
    });
}
window.addEventListener("DOMContentLoaded", ()=>{changeDimensionNew();} )


