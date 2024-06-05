// action="{{url_for('influencer.colab', campaign_id = campaign.campaign_id)}}" 

async function request_colab(url){
    try{
    const response = await fetch(url,{
                                method : 'POST',        
                                headers : {'Content-Type':'application/json'}
                                })
    const result = await response.json()
    flash(result['Request'])

    }
    catch(error){
    flash('Something Went Wrong, Try Again later')
    }
}

function flash(msg){
    const flash_cont = document.getElementById('flash_cont')
    flash_cont.innerHTML = `<div class="alert alert-secondary alert-dismissible fade show" role="alert">
                                <span>${msg}</span>
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div>`
}