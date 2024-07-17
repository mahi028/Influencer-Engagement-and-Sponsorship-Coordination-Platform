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

async function flag_camp(camp_id, reason){
    let rqst = await post_rqst(`/admin/flag/camp/${camp_id}/${reason}`)
    console.log(camp_id)
    if (rqst['Request'] === 'Success'){
        const flag_cont = document.getElementById('flag_cont'+camp_id)
        const flag_btn = document.getElementById('camp'+camp_id)
        if (flag_btn.innerHTML  === 'Flag'){
            flag_cont.innerHTML = `<button type="button" class="btn btn-danger" id="camp${camp_id}" onclick="flag_camp('${camp_id}', 'none')">Un-Flag</button>`
        }else{
            flag_cont.innerHTML = `  <div class="btn-group">
                                        <button type="button" class="btn btn-info dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                                            <span id="camp${camp_id}">Flag</span>
                                        </button>
                                        <ul class="dropdown-menu">
                                            <li><button class="dropdown-item" onclick="flag_camp('${camp_id}', 'Hateful_or_targeting')">Hateful or targeting</button></li>
                                            <li><button class="dropdown-item" onclick="flag_camp('${camp_id}', 'spam')">Spam</button></li>
                                            <li><button class="dropdown-item" onclick="flag_camp('${camp_id}', 'inapropriate_content')">Inapropriate Content</button></li>
                                        </ul>
                                    </div>
                                `
        }
    }
}
async function flag_user(user_id, reason){
    let rqst = await post_rqst(`/admin/flag/user/${user_id}/${reason}`)
    if (rqst['Request'] === 'Success'){
        const flag_cont = document.getElementById('flag_cont'+user_id)
        const flag_btn = document.getElementById('user'+user_id)
        if (flag_btn.innerHTML  === 'Flag'){
            flag_cont.innerHTML = `<button type="button" class="btn btn-danger" id="user${user_id}" onclick="flag_user('${user_id}', 'none')">Un-Flag</button>`
        }else{
            flag_cont.innerHTML = ` <div class="btn-group">
                                        <button type="button" class="btn btn-info dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                                            <span id="user${user_id}">Flag</span>
                                        </button>
                                        <ul class="dropdown-menu">
                                            <li><button class="dropdown-item" onclick="flag_user('${user_id}', 'inapropriate_user')">Inapropriate User</button></li>
                                            <li><button class="dropdown-item" onclick="flag_user('${user_id}', 'spam')">Spam</button></li>
                                            <li><button class="dropdown-item" onclick="flag_user('${user_id}', 'inapropriate_content')">Inapropriate Content</button></li>
                                        </ul>
                                    </div>
                                `
        }
    }
}

async function delete_camp(campaign_id){
    let rqst = await post_rqst(`/sponser/delete/campaign/${campaign_id}`)
    if (rqst['Request'] === 'Success'){
        window.location.href = '/dashboard'
    }
}