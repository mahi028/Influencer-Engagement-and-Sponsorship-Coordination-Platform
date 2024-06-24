async function make_response(url, to_update, value){
    try{
        const response = await fetch(url,{
                                    method : 'PUT',        
                                    headers : {'Content-Type':'application/json'},
                                    body : JSON.stringify({'to_update' : to_update, 'value' : value})
                                    })
        const result = await response.json()
        flash(result['Request'])
        return result

    }catch(error){
        flash('Something Went Wrong, Try Again later')
        return {'Request' : 'Unsuccessful'}
    }
}

async function profile_edit(url, tag_id, to_update){
    let value = document.getElementById('inp'+tag_id).value
    result = await make_response(url, to_update, value)
    if (result['Request'] === 'Success'){
        const tag = document.getElementById(tag_id)
        new_value = `${result['new_val']} <button type="button" class="btn" onclick="profile_edit_form('${url}', '${tag_id}', '${to_update}')"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16"><path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001m-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708z"></path></svg></button>` 
        tag.innerHTML = new_value
    }else{
        flash(result['Request'])
    }
}

function profile_edit_form(url, tag_id, to_update){
    const tag = document.getElementById(tag_id)
    let input = `<input type = "text" id = '${'inp'+tag_id}'><button class = "btn" onclick="profile_edit('${url}', '${tag_id}','${to_update}')"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send-check" viewBox="0 0 16 16"><path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855a.75.75 0 0 0-.124 1.329l4.995 3.178 1.531 2.406a.5.5 0 0 0 .844-.536L6.637 10.07l7.494-7.494-1.895 4.738a.5.5 0 1 0 .928.372zm-2.54 1.183L5.93 9.363 1.591 6.602z"/><path d="M16 12.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0m-1.993-1.679a.5.5 0 0 0-.686.172l-1.17 1.95-.547-.547a.5.5 0 0 0-.708.708l.774.773a.75.75 0 0 0 1.174-.144l1.335-2.226a.5.5 0 0 0-.172-.686"/></svg></button>`
    tag.innerHTML = input
}