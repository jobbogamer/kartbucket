
var newTrackID = -1;
var newPersonID = -1;
var newProofURL = "";
var useFileUpload = true;

function prepareEditModal(trackID, trackName, personID, personName, character, kart, wheels, glider, choiceOfKart, allowsCustomisation)
{
    $("#edit-modal .modal-title").html("Submit Time - " + trackName);
    $("#edit-modal-error-message").hide();

    $("#edit-modal-person-field").html(personName);

    $("#edit-modal-time-field").val("");
    $("#edit-modal-split1-field").val("");
    $("#edit-modal-split2-field").val("");
    $("#edit-modal-split3-field").val("");

    $("#edit-modal-character-field").val(character);
    $("#edit-modal-kart-field").val(kart);
    $("#edit-modal-wheels-field").val(wheels);
    $("#edit-modal-glider-field").val(glider);

    $("#edit-modal-upload-field").val(null);
    $("#edit-modal-url-field").val("")
    $("#proof-url").html("");
    $("#upload-indicator").html('<a href="#" onclick="useURLForProof()"><i class="fa fa-fw fa-link"></i></a>');

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

function prepareInfoModal(trackID, trackName, personID, personName)
{
    $("#info-modal .modal-title").html(personName + "'s Time - " + trackName);

    $.ajax({
        url: '/api/time',
        data: {
            'track' : trackID,
            'person': personID
        }
    }).done(function(result) {
        if (result['success']) {
            
        } else {
            $("#info-modal-error-content").html(result['message']);
            $("#info-modal-error-message").show();
            $("#info-modal-content").hide();
        }
    }).fail(function() {
        $("#info-modal-error-content").html("The server could not be contacted, or an error occurred.");
        $("#info-modal-error-message").show();
        $("#info-modal-content").hide();
    });
}


function submitTime()
{
    $("#edit-modal-error-message").slideUp();

    var time = $("#edit-modal-time-field").val();
    var split1 = $("#edit-modal-split1-field").val();
    var split2 = $("#edit-modal-split2-field").val();
    var split3 = $("#edit-modal-split3-field").val();

    var character = $("#edit-modal-character-field").val();
    var kart = $("#edit-modal-kart-field").val();
    var wheels = $("#edit-modal-wheels-field").val();
    var glider = $("#edit-modal-glider-field").val();

    if (useFileUpload)
    {
        var proof = newProofURL;
    }
    else
    {
        var proof = $("#edit-modal-url-field").val();
    }

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
            'proof': proof
        }
    }).done(function(result) {
        if (result['success']) {
            $("#time-" + newTrackID + "-" + newPersonID + " .time").html(time);
            $("#character-" + newTrackID + "-" + newPersonID).html(character);
            $("#kart-" + newTrackID + "-" + newPersonID).html(kart);
            $("#wheels-" + newTrackID + "-" + newPersonID).html(wheels);
            $("#glider-" + newTrackID + "-" + newPersonID).html(glider);
            $("#edit-modal").modal('hide');
        } else {
            $("#edit-modal-error-content").html(result['message']);
            $("#edit-modal-error-message").slideDown();
        }
    });
}

function uploadToImgur(file, form)
{
    $("#upload-indicator").html('<i class="fa fa-fw fa-spin fa-spinner"></i>');
    $("#edit-modal-submit-button").prop("disabled", true);
    $("#edit-modal-cancel-button").prop("disabled", true);

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
        $("#upload-indicator").html('<i class="fa fa-fw fa-check"></i>');
        $("#edit-modal-submit-button").prop("disabled", false);
        $("#edit-modal-cancel-button").prop("disabled", false);
        form.value = null;
    }
    xhr.setRequestHeader('Authorization', 'Client-ID d8f7791810ee729');
    xhr.send(fd);
}

function useFileForProof()
{
    useFileUpload = true;
    $("#url-field").slideUp();
    $("#upload-field").slideDown();
}

function useURLForProof()
{
    useFileUpload = false;
    $("#upload-field").slideUp();
    $("#url-field").slideDown();
}
