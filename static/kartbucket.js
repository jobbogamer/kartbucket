
var newTrackID = -1;
var newPersonID = -1;
var newProofURL = "";

function prepareEditModal(trackID, trackName, personID, personName, character, kart, wheels, glider, choiceOfKart, allowsCustomisation)
{
    $("#edit-modal .modal-title").html("Submit Time - " + trackName);

    $("#edit-modal-person-field").val(personID);

    $("#edit-modal-time-field").val("");
    $("#edit-modal-split1-field").val("");
    $("#edit-modal-split2-field").val("");
    $("#edit-modal-split3-field").val("");

    $("#edit-modal-character-field").val(character);
    $("#edit-modal-kart-field").val(kart);
    $("#edit-modal-wheels-field").val(wheels);
    $("#edit-modal-glider-field").val(glider);

    $("#edit-modal-proof-field").val(null);
    $("#proof-url").html("");
    $("#upload-indicator").html('<i class="fa fa-fw fa-circle-o"></i>');

    if (!allowsCustomisation)
    {
        $("#wheels-field").hide();
        $("#glider-field").hide();

        if (!choiceOfKart)
        {
            $("#kart-field").hide();
        }
    }

    newTrackID = trackID;
    newPersonID = personID;
}

function submitTime()
{
    var time = $("#edit-modal-character-field").val();
    var split1 = $("#edit-modal-character-field").val();
    var split2 = $("#edit-modal-character-field").val();
    var split3 = $("#edit-modal-character-field").val();

    var character = $("#edit-modal-character-field").val();
    var kart = $("#edit-modal-kart-field").val();
    var wheels = $("#edit-modal-wheels-field").val();
    var glider = $("#edit-modal-glider-field").val();

    $.ajax({
        url: '/api/submit',
        data: {
            'track' : newTrackID,
            'person': newPersonID,
            'time': time,
            'split1': split1,
            'split2': split2,
            'split3': split3,
            'character': character,
            'kart': kart,
            'wheels': wheels,
            'glider': glider,
            'proof': newProofURL
        }
    }).done(function(result) {
        if (result['success']) {
            
        } else {

        }
    });
}

function uploadToImgur(file, form)
{
    $("#upload-indicator").html('<i class="fa fa-fw fa-spin fa-circle-o-notch"></i>');
    if (!file || !file.type.match(/image.*/)) return;
    var fd = new FormData();
    fd.append("image", file);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https://api.imgur.com/3/image.json");
    xhr.onload = function() {
        var result = JSON.parse(xhr.responseText).data.link;
        newProofURL = result;
        $("#proof-url").html('<a target="_blank" href="' + newProofURL + '">' + newProofURL + '</a>');
        $("#proof-url").slideDown();
        $("#upload-indicator").html('<i class="fa fa-fw fa-circle"></i>');
        form.value = null;
    }
    xhr.setRequestHeader('Authorization', 'Client-ID d8f7791810ee729');
    xhr.send(fd);
}
