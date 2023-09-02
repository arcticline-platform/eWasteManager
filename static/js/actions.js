var btn = document.getElementsByClassName('confirmBtn')
for (var i = 0; i < btn.length; i++) {
    btn[i].addEventListener('click', function(e) {
        e.preventDefault();
        var ewasteId = this.dataset.item
        var action = this.dataset.action
        console.log('ewasteId:', ewasteId, 'action:', action)
        updateEWasteStatus(ewasteId, action)

    })
}
function updateEWasteStatus(ewasteId, action, order) {
    console.log('Attempting to Send Data');

    if (action == 'confirm') {
        var url = '/ewaste/confirm_status/'
    }
    console.log("Sending...");
    $.ajax({
        headers: { 'X-CSRFToken': csrftoken },
        type: 'POST',
        url: url,
        data: { 'ewasteId': ewasteId, 'action': action, 'order': order},
        beforeSend: function() {
            var action = '.actions'
            action += ewasteId
            console.log(action);
            $(action).hide(); // Hide the add to cart button
        },
        success: function update_content(str) {
            console.log("Status Updated!");
            var html = ``;
            var injection = '.alert';
            injection += ewasteId;
            html += `<p>You have updated Item Status!</p>`;
            document.querySelector(injection).innerHTML = html;
            
        },
        error: function() {
            console.log("Error Updating Item Status!");
        },
    });
}