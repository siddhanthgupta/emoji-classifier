$(function () {

    var data_radar = {
        labels: ["Happy", "Sad", "Angry", "Confused"],
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

    function handleEmojiClick() {
        var emoji_classes = $(this).attr("class").split(' ');
        var emoji_particular = emoji_classes[1]
            // var image = $(this).css("background-image");
        $.ajax({
            url: "/emojiDetails",
            contentType: "application/json",
            data: JSON.stringify({
                "name": emoji_particular
            }),
            type: "POST",
            success: function (response) {
                var response_data = $.parseJSON(response);
                if ("error" in response_data) {
                    emojiErrorHandler(response_data["error"]);
                } else {
                    $("#initial-emoji-placeholder").hide();
                    var bigass_emoji = $(".big-emoji");
                    var big_classes = bigass_emoji.attr("class").split(' ');
                    if (big_classes.length > 1) {
                        bigass_emoji.removeClass(big_classes[big_classes.length - 1]);
                    }
                    bigass_emoji.addClass(emoji_particular);
                    $("#classification-data").show();
                    $("#name").text(response_data["name"]);
                    $("#classification").text("Classified as " +
                    response_data["classification"] + " with " + response_data["accuracy"] + "% accuracy");
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


    $(".emotion-tab").on("click", function () {
        var emotion = $(this).text().toLowerCase();
        $("#initial-emoji-placeholder").text("Select an emoji to see classification");
        var emotionList = emotion + "-list";
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
                    emotionListElement.append($('<div class="emoji ' +
                        emotion_class + '">').on("click", handleEmojiClick));
                }
            },
            error: function (error) {}
        });
    });

    $(".emoji").on("click", function () {
        handleEmojiClick();
    });

});
