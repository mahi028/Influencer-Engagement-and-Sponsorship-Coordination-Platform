function flash(msg){
    const flash_cont = document.getElementById('flash_cont');
    flash_cont.innerHTML = `<div class="alert alert-primary alert-dismissible fade show" role="alert">
                                <span>${msg}</span>
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div>`;
}