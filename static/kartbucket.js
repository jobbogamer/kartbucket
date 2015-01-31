
var newTrackID = -1;
var newPersonID = -1;

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
            'glider': glider
        }
    }).done(function(result) {
        if (result['success']) {
            
        } else {

        }
    });
}
