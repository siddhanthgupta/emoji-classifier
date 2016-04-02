$(function () {

    var data_radar = {
        labels: ["Happy", "Sad", "Angry", "Confused", "Fear", "Disgust"],
        datasets: [{
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            // data: [28, 65, 27, 34]
        }]
    };
    $("#classification-data").hide();

    function emojiErrorHandler(error) {
        console.log(error);
        $("#classification-data").hide();
        $("#initial-emoji-placeholder").text("An error occurred. Please try again.");
        $("#initial-emoji-placeholder").show();
    };

    function emojiDetails(image, imageNameWithoutExtension) {
        $.ajax({
            url: "/emojiDetails",
            contentType: "application/json",
            data: JSON.stringify({
                "name": imageNameWithoutExtension
            }),
            type: "POST",
            success: function (response) {
                var response_data = $.parseJSON(response);
                if ("error" in response_data) {
                    emojiErrorHandler(response_data["error"]);
                } else {
                    $("#initial-emoji-placeholder").hide();
                    var bigass_emoji = $(".big-emoji");
                    // var big_classes = bigass_emoji.attr("class").split(' ');
                    // if (big_classes.length > 1) {
                    //     bigass_emoji.removeClass(big_classes[big_classes.length - 1]);
                    // }
                    // bigass_emoji.addClass(emoji_particular);
                    bigass_emoji.css('background-image', image);
                    $("#classification-data").show();
                    $("#name").text(response_data["name"]);
                    if (response_data["classification"].toLowerCase().localeCompare("miscellaneous") == 0) {
                        $("#classification").text("Classified as " + response_data["classification"]);
                    } else {
                        $("#classification").text("Classified as " +
                            response_data["classification"] + " with " + parseFloat(response_data["accuracy"]).toFixed(2) + "% certainty");
                    }
                    data_radar["datasets"][0]["data"] = response_data["data"].slice();
                    var ctx = $("#accuracy-chart").get(0).getContext("2d");
                    var myRadarChart = new Chart(ctx).Radar(data_radar);
                }
            },
            error: function (error) {
                emojiErrorHandler(error);
            }
        });
    };

    function handleEmojiClick() {
        // var emoji_classes = $(this).attr("class").split(' ');
        // var emoji_particular = emoji_classes[1]
        // console.log(emoji_particular);
        var image = $(this).css("background-image");
        console.log(image);
        var splitImage = image.split('/');
        var imageNameWithGarbage = splitImage[splitImage.length - 1];
        var imageNameWithExtension = imageNameWithGarbage.substr(0, imageNameWithGarbage.length - 2);
        var imageNameWithoutExtension = imageNameWithExtension.split('.')[0];

        console.log('emoji-' + imageNameWithoutExtension);
        emojiDetails(image, imageNameWithoutExtension);
    };


    $(".emotion-tab").on("click", function () {
        var emotion = $(this).text().toLowerCase();
        if (emotion.localeCompare('misc') == 0) {
            emotion = 'miscellaneous';
        }
        $("#initial-emoji-placeholder").text("Select an emoji to see classification");
        var emotionList = emotion + "-list";
        console.log(emotionList);
        $.ajax({
            url: "/emojiList",
            contentType: "application/json",
            data: JSON.stringify({
                "emotion": emotion
            }),
            type: "POST",
            success: function (response) {
                var response_data = $.parseJSON(response);
                var emotionListElement = $("#" + emotionList);
                emotionListElement.empty();
                for (i in response_data["list"]) {
                    var emotion_class = "emoji-" + response_data["list"][i];
                    emotionListElement.append($('<div class="emoji">').css('background-image', 'url("/static/emojis/' + response_data["list"][i] + '.png")').on("click", handleEmojiClick));
                }
            },
            error: function (error) {}
        });
    });

    // $('#file-dropzone').dropzone({
    //     url: "/upload",
    //     maxFilesize: 1,
    //     maxFiles: 1,
    //     // addRemoveLinks:true,
    //     paramName: "emoticon_file",
    //     acceptedFiles: "image/png",
    //     maxThumbnailFilesize: 5,
    //     // removedfile: function(file) {
    //     //   var fileRef;
    //     //   return (fileRef = file.previewElement) != null ?
    //     // 	      fileRef.parentNode.removeChild(file.previewElement) : void 0;
    //     //     },
    //     init: function () {
    //
    //         this.on('success', function (file, response) {
    //             var fileRef;
    //             if ((fileRef = file.previewElement) != null) {
    //                 fileRef.parentNode.removeChild(file.previewElement);
    //             }
    //             $('#upload-modal').modal('hide');
    //             console.log(response)
    //
    //         });
    //
    //         this.on('addedfile', function (file) {
    //             // alert('wut');
    //         });
    //
    //         this.on('drop', function (file) {
    //             // alert('file');
    //         });
    //     }
    // });

    var lastTarget = null;

    function isFile(evt) {
        var dt = evt.dataTransfer;

        for (var i = 0; i < dt.types.length; i++) {
            if (dt.types[i] === "Files") {
                return true;
            }
        }
        return false;
    }

    window.addEventListener("dragenter", function (e) {
        if (isFile(e)) {
            lastTarget = e.target;
            document.querySelector("#dropzone").style.visibility = "";
            document.querySelector("#dropzone").style.opacity = 1;
            document.querySelector("#textnode").style.fontSize = "48px";
        }
    });

    window.addEventListener("dragleave", function (e) {
        e.preventDefault();
        if (e.target === lastTarget) {
            document.querySelector("#dropzone").style.visibility = "hidden";
            document.querySelector("#dropzone").style.opacity = 0;
            document.querySelector("#textnode").style.fontSize = "42px";
        }
    });

    window.addEventListener("dragover", function (e) {
        e.preventDefault();
    });

    window.addEventListener("drop", function (e) {
        e.preventDefault();
        document.querySelector("#dropzone").style.visibility = "hidden";
        document.querySelector("#dropzone").style.opacity = 0;
        document.querySelector("#textnode").style.fontSize = "42px";
        if (e.dataTransfer.files.length == 1) {
            // document.querySelector("#text").innerHTML =
            //     "<b>File selected:</b><br>" + e.dataTransfer.files[0].name;
            console.log(e.dataTransfer.files[0])
            var file_to_send = e.dataTransfer.files[0];
            var form = new FormData();
            form.append('emoticon_file', file_to_send);
            $.ajax({
                url: "/upload",
                contentType: false,
                processData:false,
                data: form,
                type: "POST",
                success: function (response) {
                    var response_data = $.parseJSON(response);
                    console.log('Data sent');
                    console.log(response_data);
                    if('error' in response_data) {
                        emojiErrorHandler(response_data['error'])
                    } else {
                        var filename = response_data['name'].substr(0, response_data['name'].length - 4);
                        var image_url = 'url("/static/emojis/' + filename + '.png")'
                        emojiDetails(image_url, filename);
                    }
                },
                error: function (error) {
                    emojiErrorHandler(error);
                }
            });
        }
    });


});
