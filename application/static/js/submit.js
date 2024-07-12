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

async function flag_camp(camp_id){
    rqst = await post_rqst(`/admin/flag/camp/${camp_id}`)
    if (rqst['Request'] === 'Success'){
        flag_btn = document.getElementById(camp_id)
        if (flag_btn.innerHTML  === 'Flag'){
            flag_btn.innerHTML = "Un-Flag"
        }else{
            flag_btn.innerHTML = "Flag"
        }
    }
}
async function flag_user(user_id){
    rqst = await post_rqst(`/admin/flag/user/${user_id}`)
    if (rqst['Request'] === 'Success'){
        flag_btn = document.getElementById(user_id)
        if (flag_btn.innerHTML  === 'Flag'){
            flag_btn.innerHTML = "Un-Flag"
        }else{
            flag_btn.innerHTML = "Flag"
        }
    }
}

async function delete_camp(campaign_id){
    rqst = await post_rqst(`/sponser/delete/campaign/${campaign_id}`)
    if (rqst['Request'] === 'Success'){
        window.location.href = '/dashboard'
    }
}