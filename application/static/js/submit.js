// action="{{url_for('influencer.colab', campaign_id = campaign.campaign_id)}}" 

async function post_rqst(url){
    try{
        const response = await fetch(url,{
                                    method : 'POST',        
                                    headers : {'Content-Type':'application/json'}
                                    })
        const result = await response.json()
        flash(result['Request'])
        return result

    }catch(error){
        flash('Something Went Wrong, Try Again later')
        return {'Request' : 'Unsuccessful'}
    }
}

async function delete_camp(campaign_id){
    rqst = await post_rqst(`/sponser/delete/campaign/${campaign_id}`)
    if (rqst['Request'] === 'Success'){
        document.getElementById(`campaigns`).removeChild(document.getElementById(`${campaign_id}`))
    }

}