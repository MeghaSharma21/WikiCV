"use strict";
/*
    Global variable for the maximum number of pinned
    repositories the user can add
*/
var MAX_NUMBER_OF_PINNED_REPOSITORIES = 6;

// For getting csrf token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        cookies.forEach(function (element) {
            var cookie = jQuery.trim(element);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue =
                        decodeURIComponent(cookie.substring(name.length + 1));
                return;
            }
        });
    }
    return cookieValue;
}

// To check if the method is csrf Safe
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

// This is called when user clicks on edit-profile button
function editProfile() {
    $('.edit-profile-btn').attr("onclick", "saveProfile()");
    $('.edit-profile-btn').html('<i class="fa fa-save"></i> Save Profile');
    $('.edit-profile-btn').css({
        "margin-top": "-73px"
    });

    // Hide the actual divs containing info, make forms visible
    $('#external-profiles-edit-links').addClass('visible')
        .removeClass('hidden');
    $('.external-profiles-links').addClass('hidden');

    $('.edit-name-location-holder').addClass('visible').removeClass('hidden');
    $('.username').addClass('hidden');
    $('.work').addClass('hidden');

    $('.languages-input').addClass('visible').removeClass('hidden');
    $('.languages-info').addClass('hidden');

    $('.tools-input').addClass('visible').removeClass('hidden');
    $('.tools-info').addClass('hidden');

    $('.introduction-input').addClass('visible').removeClass('hidden');
    $('.introduction').addClass('hidden');

    $('.close-icon').addClass('visible').removeClass('hidden');
    $('.add-pinned-repository-btn-container')
        .addClass('visible').removeClass('hidden');

/*
 Hide Badges, these are of no use in edit profile and make
 space for inputs
*/
    $('.second-skill').css({
        "padding-top": "10px"
    });
    $('.badges').addClass('hidden');

    // Also, Hide everything else
    $('#profile-dashboard').addClass('hidden');
    $('#profile-achievements').addClass('hidden');
    $('#profile-summary').addClass('hidden');
    $('#wikimedia-summary-tab').addClass('hidden');
    $('#achievements-tab').addClass('hidden');
    $('#dashboard-tab').addClass('hidden');
}

/*
* Input: pinned_repositories_fixed : Array of pinned_repositories
*                                   which were already there
*        pinned_repositories_editable : Array of pinned_repositories
*                                  which have been added by the user now
* */
function addPinnedRepositoryToHTML(pinned_repositories_fixed,
        pinned_repositories_editable) {
    // displaying fixed repositories
    var htmlForFirstRow = '';
    var htmlForSecondRow = '';
    var nextRepository = 1;
    var indexOfFixedRepositories = 0;
    while (indexOfFixedRepositories < pinned_repositories_fixed.length
            && nextRepository <= 3) {
        htmlForFirstRow += '<div class="card pinned-repository"><span' +
                ' class="close-icon" data-effect="fadeOut">' +
                '<i class="fa fa-2x fa-times"></i></span><div' +
                ' class="card-body"><h5 class="card-title">' +
                pinned_repositories_fixed[indexOfFixedRepositories].title +
                '</h5><p class="card-text">' +
                pinned_repositories_fixed[indexOfFixedRepositories]
            .description +
                    '</p></div><div class="card-footer pinned-repository-' +
                    'info"><div class="one-half"><strong class="page-views">' +
                    pinned_repositories_fixed[indexOfFixedRepositories]
            .page_views +
                    '</strong><strong>per day</strong>Views</div><div ' +
                    'class="one-half"><strong class="contribution">' +
                    pinned_repositories_fixed[indexOfFixedRepositories]
            .percentage_contribution +
                    '</strong><strong>% by Bytes</strong>Contribution</div>' +
                    '</div></div>';

        nextRepository = nextRepository + 1;
        indexOfFixedRepositories = indexOfFixedRepositories + 1;
    }

    while (indexOfFixedRepositories < pinned_repositories_fixed.length) {
        htmlForSecondRow += '<div class="card pinned-repository">' +
                '<span class="close-icon" data-effect="fadeOut">' +
                '<i class="fa fa-2x fa-times"></i></span><div class="card' +
                '-body"><h5 class="card-title">' +
                pinned_repositories_fixed[indexOfFixedRepositories].title +
                '</h5><p class="card-text">' +
                pinned_repositories_fixed[indexOfFixedRepositories]
            .description +
                    '</p></div><div class="card-footer pinned-repository-' +
                    'info"><div class="one-half"><strong class="page-views">' +
                    pinned_repositories_fixed[indexOfFixedRepositories]
            .page_views +
                    '</strong><strong>per day</strong>Views</div>' +
                    '<div class="one-half"><strong class="contribution">' +
                    pinned_repositories_fixed[indexOfFixedRepositories]
            .percentage_contribution +
                    '</strong><strong>% by Bytes</strong>' +
                    'Contribution</div></div></div>';

        nextRepository = nextRepository + 1;
        indexOfFixedRepositories = indexOfFixedRepositories + 1;
    }

    // displaying editable repositories
    jQuery.each(pinned_repositories_editable, function (title, description) {
        if (nextRepository <= 3) {
            htmlForFirstRow += '<div class="card pinned-repository">' +
                    '<span class="close-icon" data-effect="fadeOut">' +
                    '<i class="fa fa-2x fa-times"></i></span>' +
                    '<div class="card-body"><input class="card-title" ' +
                    'placeholder="Enter Card title" value="' + title +
                    '"><br/><textarea class="card-text" ' +
                    'placeholder="Enter card description">' + description +
                    '</textarea></div><div ' +
                    'class="card-footer pinned-repository-info">' +
                    '<div class="one-half"><strong>X</strong> Views</div>' +
                    '<div class="one-half"><strong>Y% by Bytes </strong>' +
                    'Contribution</div></div></div>';
            nextRepository = nextRepository + 1;
        } else {
            htmlForSecondRow += '<div class="card pinned-repository">' +
                    '<span class="close-icon" data-effect="fadeOut">' +
                    '<i class="fa fa-2x fa-times"></i></span>' +
                    '<div class="card-body"><input class="card-title" ' +
                    'placeholder="Enter Card title" value="' + title +
                    '"><br/><textarea class="card-text" ' +
                    'placeholder="Enter card description">' + description +
                    '</textarea></div>' +
                    '<div class="card-footer pinned-repository-info">' +
                    '<div class="one-half"><strong>X</strong>Views</div>' +
                    '<div class="one-half"><strong>Y% by Bytes </strong>' +
                    'Contribution</div></div></div>';
        }
    });

    $('.pinned-repository-first-row').html(htmlForFirstRow);
    $('.pinned-repository-second-row').html(htmlForSecondRow);
}

/* Whenever pinned_repository is added or deleted, the collection
* of repositories must be realigned to make sure there are 3
* pinned_repositories in the first row before we begin to fill the second row!
* */
function reAlignPinnedRepositories() {
    var currentLength;
    // Collecting pinned repositories
    var pinned_repositories_fixed = [];
    var pinned_repositories_editable = {};
    $('.card').each(function () {
        if ($(this).find('.card-text').is('p')) {
            pinned_repositories_fixed.push({
                'title': $(this).find('.card-title').text(),
                'description': $(this).find('.card-text').text(),
                'page_views': $(this).find('.page-views').text(),
                'percentage_contribution': $(this).find('.contribution').text()
            });
        } else {
            pinned_repositories_editable[$(this).find('.card-title').val()] =
                    $(this).find('.card-text').val();
        }
    });

    addPinnedRepositoryToHTML(pinned_repositories_fixed,
            pinned_repositories_editable);

    // we have all the pinned repositories in correct position
    currentLength = Object.keys(pinned_repositories_fixed).length +
            Object.keys(pinned_repositories_editable).length;

/*
 Make the add-pinned-repository button visible if number of
 pinned_repositories < MAX_NUMBER_OF_PINNED_REPOSITORIES
*/
    if (currentLength < MAX_NUMBER_OF_PINNED_REPOSITORIES) {
        $('.add-pinned-repository').removeClass('hidden');
    }

    return currentLength;
}

/* This function adds a new repository in the UI for user to edit,
* the repository is actually added to database of WikiCV once the
* user clicks on save-profile
* */
function addPinnedRepository() {
    var currentLength = reAlignPinnedRepositories();

    // we have all the pinned repositories in correct position
    var html = '<div class="card pinned-repository">' +
            '<span class="close-icon" data-effect="fadeOut">' +
            '<i class="fa fa-2x fa-times"></i></span>' +
            '<div class="card-body"><input class="card-title" ' +
            'placeholder="Enter Card title"><br/><textarea class="card-text"' +
            ' placeholder="Enter card description"></textarea>' +
            '</div><div class="card-footer pinned-repository-info">' +
            '<div class="one-half"><strong>X</strong> Views</div>' +
            '<div class="one-half"><strong>Y% by Bytes </strong>' +
            'Contribution</div></div></div>';

    if (currentLength < 3) {
        // in first deck
        $('.pinned-repository-first-row')
            .html($('.pinned-repository-first-row').html() + html);
    } else {
        $('.pinned-repository-second-row')
            .html($('.pinned-repository-second-row').html() +
                    html);
    }

    currentLength = currentLength + 1;
    if (currentLength >= MAX_NUMBER_OF_PINNED_REPOSITORIES) {
        $('.add-pinned-repository').addClass('hidden');
    }
}

/* This is called to save the changes user has made into his profile-details,
*  Makes an AJAX call to the server, Shows error returned by the server in
*  case of an error or reloads the WikiCV page on successful transaction
*/
function saveProfile() {

    // Collecting pinned repositories
    var pinned_repositories = {};
    $('.card').each(function () {
        if ($(this).find('.card-text').is('p')) {
            pinned_repositories[$(this).find('.card-title').text()] =
                    $(this).find('.card-text').text();
        } else {
            pinned_repositories[$(this).find('.card-title').val()] =
                    $(this).find('.card-text').val();
        }
    });

    $.ajax({url: "/outreachy-wikicv/edit-profile/" + String(username) + "/",
            type: "post",
            data: {
        'full_name': $('#id_full_name').val(),
        'location': $('#id_location').val(),
        'job_designation': $('#id_work').val(),
        'languages': String($('#id_languages').val()),
        'tools': $('#id_tools').val(),
        'introduction': $('#id_introduction').val(),
        'website': $('#id_website').val(),
        'blog': $('#id_blog').val(),
        'github': $('#id_github').val(),
        'linkedin': $('#id_linkedin').val(),
        'facebook': $('#id_facebook').val(),
        'twitter': $('#id_twitter').val(),
        'pinned_repositories': JSON.stringify(pinned_repositories)
    },
            success: function (data) {
        if (data.error === 1) {
            $("#alert-message-holder").html(
                "<div class='alert alert-danger' role='alert'>" +
                String(data.error_message) + "</div>"
            );
        } else {
            window.location.reload(true);
        }
    },
            error: function () {
        $("#alert-message-holder").html(
            "<div class='alert alert-danger' role='alert'>" +
            "<strong>Oh snap!</strong>Something went wrong while" +
            " saving updated information! Please report Megha " +
            "at meghasharma4910@gmail.com</div>"
        );
    }});
}

/* Function to select the correct tab while scrolling */
function onScroll() {
    var currentPosition = $(document).scrollTop();
    $("#profile-tabs div").each(function () {
        var element = $(this);
        var scrollTarget = $("#" + element.attr("scroll-target"));
        var scrollOffset = parseInt(element.attr("scroll-offset")) + 30;
        if (scrollTarget.position() &&
                scrollTarget.position().top - scrollOffset <= currentPosition &&
                scrollTarget.position().top + scrollTarget.height() >
                currentPosition) {
            $("#profile-tabs .tab-underline-blue .tab div")
                .removeClass("selected");
            element.parent().addClass("selected");
        }
    });
}

$(window).scroll(function () {
    var height = 170;
    if ($(this).scrollTop() >= height) {
        $("#profile-card-header").removeClass("hidden").addClass("visible");
    } else {
        $("#profile-card-header").removeClass("visible").addClass("hidden");
    }
    onScroll();
    var b = $("#profile-card-header").height();
    $("#profile-tabs").sticky({
        topSpacing: b + 3,
        bottomSpacing: 400
    });
    $("#profile-tabs-sticky-wrapper").css({
        height: "50px"
    });
});

/* Function to start the Achievements Carousel from first step */
function initializeAchievements() {
    $('.first-step div').addClass('circle-lg').removeClass('circle-sm');
    $('.first-step span').addClass('text-lg').removeClass('text-sm');
    $('.first-step h5').addClass('heading-lg').removeClass('heading-sm');
    $('.carousel-item:first').addClass('active');
}

/* Function to draw Spread Over Projects Graph
 * Input: An array of arrays, where the inner array is
 * ['Project Name', 'Total Contribution in that Project']
 * */
function drawPieChart(spread_over_projects_data) {
    var data = google.visualization.arrayToDataTable(spread_over_projects_data);
    var options = {
        title: 'Percentage contribution amongst different projects',
        width: 800,
        height: 450,
        chartArea: {
            width: '95%'
        }
    };

    var chart = new google.visualization.PieChart(document
        .getElementById('piechart'));

    chart.draw(data, options);
}

/* Function to draw Contribution distribution Graph
*  Input: An array of percentage of users in a particular group, the group
*  to which username belongs, and username
* */
function drawBarChart(contribution_distribution, user_group, username) {

    var input_data = [['Edits', 'Percentage of Users', {role: 'annotation'}]];
    var groups = ["", "O Edits", "1 Edit", "2-10 Edits", "11-50 Edits",
            "51-100 Edits", "100-500 Edits", "501-1000 Edits",
            "More than 1000 Edits"];
    var annotation = String(username) + " belongs to this group";
    contribution_distribution.forEach(function (value, index) {
        if (index === 0) {
            return;
        }
        if (index === user_group) {
            input_data.push([groups[index], value, annotation]);
        } else {
            input_data.push([groups[index], value, '']);
        }
    });

    var data = google.visualization.arrayToDataTable(input_data);

    var options = {
        title: 'Distribution of Users considering edits',
        width: 800,
        height: 400,
        hAxis: {
            title: 'Percentage of Users',
            minValue: 0,
            maxValue: 100
        },
        chartArea: {
            width: '55%'
        }
    };

    var chart = new google.visualization.BarChart(document
        .getElementById('bar-chart'));

    chart.draw(data, options);
}

/* Function to draw Contribution activity chart
 * Input: Articles Created Data or Articles Edited Data : JsonArray
 * of Dates and no. of contribution made on that day*/
function drawCalendarChart(inputDataArray, typeId, elementId) {
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({
        type: 'date',
        id: 'Date'
    });
    dataTable.addColumn({
        type: 'number',
        id: typeId
    });
    var graphData = [];
    (Object.keys(inputDataArray)).forEach(function (date) {
        var dateArray = date.split('-');
        graphData.push([new Date(dateArray[0], Number(dateArray[1]) - 1,
                dateArray[2]), inputDataArray[date]]);
    });
    dataTable.addRows(graphData);

    var chart = new google.visualization.Calendar(document
        .getElementById(elementId));

    var options = {
        title: typeId,
        calendar: {cellSize: 14}
    };

    chart.draw(dataTable, options);
}

/* Function to draw Contribution activity chart
*  Input: JSON Object whose key is month and value is that month's impact
* */
function drawColumnChart(impact_data) {
    var graph_data = [];
    var all_pages = ['Page IDs'];
    var months = {'0': 'Jan', '1': 'Feb', '2': 'Mar', '3': 'Apr', '4': 'May',
            '5': 'June', '6': 'July', '7': 'Aug', '8': 'Sept', '9': 'Oct',
            '10': 'Nov', '11': 'Dec'};

    jQuery.each(impact_data, function (monthNumber, dict) {
        jQuery.each(dict, function (pageId) {
            all_pages.push(String(pageId));
        });
    });

    graph_data.push(all_pages);
    jQuery.each(months, function (monthNumber, monthName) {
        graph_data.push([monthName]);
    });

    all_pages.forEach(function (pages, index) {
        if (index) {
            jQuery.each(months, function (monthNumber) {
                graph_data[parseInt(monthNumber) + 1]
                    .push(impact_data[parseInt(monthNumber)][pages] || 0);
            });
        }
    });

    var data = new google.visualization.DataTable();
    data = google.visualization.arrayToDataTable(graph_data);

    var options = {
        width: 800,
        height: 550,
        legend: {position: 'top', maxLines: 3},
        bar: {groupWidth: '55%'},
        isStacked: true
    };

    var chart = new google.visualization.ColumnChart(document
        .getElementById('impact-graph'));

    chart.draw(data, options);
}

/* Function to draw Indicators for Achievement Carousel */
function createAchievementsIndicators(achievementData,
        leftmostAchievementIndex, rightmostAchievementIndex) {
    // in achievementData array, indexes are 0 based
    var index = leftmostAchievementIndex - 1;

    if (index < rightmostAchievementIndex) {
        $('.first-step').addClass('visible').removeClass('hidden');
        $('.first-step span').text(achievementData[index].date);
        $('.first-step h5').text(achievementData[index].heading);
    } else {
        $('.first-step').addClass('hidden').removeClass('visible');
    }
    index = index + 1;
    if (index < rightmostAchievementIndex) {
        $('.second-step').addClass('visible').removeClass('hidden');
        $('.second-step span').text(achievementData[index].date);
        $('.second-step h5').text(achievementData[index].heading);
    } else {
        $('.second-step').addClass('hidden').removeClass('visible');
    }
    index = index + 1;
    if (index < rightmostAchievementIndex) {
        $('.third-step').addClass('visible').removeClass('hidden');
        $('.third-step span').text(achievementData[index].date);
        $('.third-step h5').text(achievementData[index].heading);
    } else {
        $('.third-step').addClass('hidden').removeClass('visible');
    }
    index = index + 1;
    if (index < rightmostAchievementIndex) {
        $('.fourth-step').addClass('visible').removeClass('hidden');
        $('.fourth-step span').text(achievementData[index].date);
        $('.fourth-step h5').text(achievementData[index].heading);
    } else {
        $('.fourth-step').addClass('hidden').removeClass('visible');
    }
    index = index + 1;
    if (index < rightmostAchievementIndex) {
        $('.fifth-step').addClass('visible').removeClass('hidden');
        $('.fifth-step span').text(achievementData[index].date);
        $('.fifth-step h5').text(achievementData[index].heading);
    } else {
        $('.fifth-step').addClass('hidden').removeClass('visible');
    }
}

/* Function to return the correct image for badge */
function badgeMedalImageSource(type) {
    switch (type) {
    case 'gold':
        return '/outreachy-wikicv/static/user_summary/img/goldmedal1.png';
    case 'silver':
        return '/outreachy-wikicv/static/user_summary/img/silvermedal1.png';
    case 'bronze':
        return '/outreachy-wikicv/static/user_summary/img/bronzemedal1.png';
    }
}

$(document).ready(function () {

    // Acquiring csrf token
    var csrftoken = getCookie('csrftoken');

    // Making sure csrf token is sent with every ajax request
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    google.charts.load('current', {'packages': ['corechart', 'calendar',
            'bar']});

    // Ajax call to update data for username on server
    $.ajax({url: "/outreachy-wikicv/update-cached-data/" + String(username),
            success: function (data) {
        if (data.result) {
            alert("Your data has been updated on server." +
                    " Please refresh the page.");
        }
    }});

/*
 Whenever time filter is changed for activity and spread over projects,
 change the graphs
*/
    $('input.time-filter').on('change', function () {
        $('input.time-filter').not(this).prop('checked', false);
        $.ajax({url: "/outreachy-wikicv/load-graphs/",
                type: "get",
                data: {
            username: String(username),
            filter: String(this.value),
            time_filter_type: "general"
        },
                success: function (data) {
            google.charts.setOnLoadCallback(function () {
                drawPieChart(data.spread_over_projects_data);
                drawCalendarChart(data.created_activity_chart_data,
                        'Articles Created', 'articles-created');
                drawCalendarChart(data.edits_activity_chart_data,
                        'Articles Edited', 'articles-edited');
            });
        },
                error: function () {
            $("#alert-message-holder").html(
                "<div class='alert alert-danger' role='alert'><strong>" +
                "Oh snap!</strong>Something went wrong while creating" +
                " graphs! Please report Megha at " +
                "meghasharma4910@gmail.com</div>"
            );
        }});
    });


    //Whenever time filter is changed for impact, change the graph
    $('input.impact-time-filter').on('change', function () {
        $('input.impact-time-filter').not(this).prop('checked', false);
        $.ajax({url: "/outreachy-wikicv/load-graphs/",
                type: "get",
                data: {
            username: String(username),
            filter: String(this.value),
            time_filter_type: "year"
        },
                success: function (data) {
            google.charts.setOnLoadCallback(function () {
                drawColumnChart(data.impact_graphs_data);
            });
        },
                error: function () {
            $("#alert-message-holder").html(
                "<div class='alert alert-danger' role='alert'><strong>" +
                "Oh snap!</strong>Something went wrong while creating" +
                " graphs! Please report Megha at" +
                " meghasharma4910@gmail.com</div>"
            );
        }});
    });

    // Draw the contribution Distribution graph
    google.charts.setOnLoadCallback(function () {
        drawBarChart(percentage_of_users_in_group, user_group, username);
    });

    // Load Pinned Repositories
    addPinnedRepositoryToHTML(pinned_repositories_of_user, {});
    $('.close-icon').each(function () {
        $(this).addClass('hidden');
    });

    // Whenever navigation-tab is clicked, scroll to that section
    $(".fast-scroll").click(function () {
        var b = $(this);
        var c = $("#" + b.attr("scroll-target"));
        var d = b.attr("scroll-offset");
        if (d) {
            $("html,body").animate({
                scrollTop: c.offset().top - d
            }, "fast");
        } else {
            $("html,body").animate({
                scrollTop: c.offset().top
            }, "fast");
        }
    });

    // Toggling the caret and visibility of filters
    $(".toggle-time-filters").click(function () {
        if ($(".time-filter-caret").hasClass("fa-caret-down")) {
            $(".time-filter-caret").removeClass("fa-caret-down")
                .addClass("fa-caret-up");
            $(".valid-time-filters").each(function () {
                $(this).removeClass("hidden").addClass("visible");
            });
        } else {
            $(".time-filter-caret").removeClass("fa-caret-up")
                .addClass("fa-caret-down");
            $(".valid-time-filters").each(function () {
                $(this).removeClass("visible").addClass("hidden");
            });
        }
    });

/*
 Change the graphs and time filters for the graph which has been
 selected via radio button
*/
    $('input:radio[name="graph"]').change(function () {
        $('.graph').each(function () {
            $(this).addClass("hidden");
        });
        $('.toggle-time-filters').removeClass('hidden').addClass("visible");
        $("#time-filters-div").removeClass("invalid-time-filters")
            .addClass("valid-time-filters");
        $('#time-filters-div-impact').addClass("invalid-time-filters")
            .removeClass("valid-time-filters");
        switch (this.value) {
        case 'activity-chart':
            $('#articles-edited').removeClass("hidden").addClass("visible");
            $('#articles-created').removeClass("hidden")
                .addClass("visible");
            break;
        case 'impact':
            $('#impact-graph').removeClass("hidden").addClass("visible");
            $('#time-filters-div-impact')
                .removeClass("invalid-time-filters")
                .addClass("valid-time-filters");
            $("#time-filters-div").addClass("invalid-time-filters")
                .removeClass("valid-time-filters");
            break;
        case 'edits-distribution':
            $('#bar-chart').removeClass("hidden").addClass("visible");
            $('.toggle-time-filters').removeClass('visible')
                .addClass("hidden");
            $('#time-filters-div-impact').addClass("invalid-time-filters")
                .removeClass("valid-time-filters");
            $("#time-filters-div").addClass("invalid-time-filters")
                .removeClass("valid-time-filters");
            break;
        case 'spread-over-projects':
            $('#piechart').removeClass("hidden").addClass("visible");
            break;
        }
        // Open the relevant filters
        $(".time-filter-caret").removeClass("fa-caret-down")
            .addClass("fa-caret-up");
        $(".valid-time-filters").each(function () {
            $(this).removeClass("hidden").addClass("visible");
        });
        $(".invalid-time-filters").each(function () {
            $(this).removeClass("visible").addClass("hidden");
        });
    });

    // On page load, assign values to impact-filters
    $('input#impact-present-year').val((new Date()).getFullYear());
    $('input#impact-last-year').val((new Date()).getFullYear() - 1);
    $('input#impact-last-to-last-year').val((new Date()).getFullYear() - 2);

    // On page load, check the default filter
    $('input.default-time-filter').prop('checked', true).change();

    // On page load, show the activity graph
    $("input[name=graph][value='activity-chart']").prop("checked", true)
        .change();

    // Pinned repositories editing
    $("body").on("click", ".close-icon", function () {
        $(this).closest('.card').remove();
        reAlignPinnedRepositories();
    });

    // Achievements Carousel
    var achievementData = [];
    var helperJson = {'GA': 'Good Article',
            'FA': 'Featured Article',
            'A': 'Grade A Article'};
    achievements.forEach(function (value) {
        achievementData.push({
            "date": String(value.percentage_contribution) + "%",
            "heading": helperJson[String(value.type)]
        });
    });

    var noOfAchievementsVisible = 5;
    var leftmostAchievementIndex = 1;
    var rightmostAchievementIndex = Math.min(achievementData.length,
            noOfAchievementsVisible);
/*
 Window will shift by slidingWindowConstant whenever we'll
 reach the end of visible region
*/
    var slidingWindowConstant = 5;
    var stepsOffBy = leftmostAchievementIndex - 1;
    createAchievementsIndicators(achievementData, leftmostAchievementIndex,
            rightmostAchievementIndex);
    initializeAchievements();

    $('#myCarousel').carousel();
    $('#myCarousel').on('slide.bs.carousel', function (e) {

        $('.achievement-date').each(function () {
            $(this).addClass('text-sm').removeClass('text-lg');
        });

        $('.achievement-circle').each(function () {
            $(this).addClass('circle-sm').removeClass('circle-lg');
        });

        $('.achievement-heading').each(function () {
            $(this).addClass('heading-sm').removeClass('heading-lg');
        });

        //update progress
        var step = $(e.relatedTarget).data('step');

        // Edge cases to handle wrap around
        if (step === 1) {
            leftmostAchievementIndex = 1;
            rightmostAchievementIndex = Math.min(achievementData.length,
                    noOfAchievementsVisible);
        }

        if (step === achievementData.length) {
            rightmostAchievementIndex = achievementData.length;
            leftmostAchievementIndex = Math.max(1,
                    rightmostAchievementIndex - noOfAchievementsVisible + 1);
        }

        // Sliding window
        if (step < leftmostAchievementIndex) {
            leftmostAchievementIndex = Math
                .max(leftmostAchievementIndex - slidingWindowConstant,
                        1);
            rightmostAchievementIndex = Math.min(achievementData.length,
                    leftmostAchievementIndex + noOfAchievementsVisible - 1);
        }

        if (step > rightmostAchievementIndex) {
            rightmostAchievementIndex = Math
                .min(rightmostAchievementIndex + slidingWindowConstant,
                        achievementData.length);
            leftmostAchievementIndex = Math.max(1, rightmostAchievementIndex -
                    noOfAchievementsVisible + 1);
        }

        createAchievementsIndicators(achievementData,
                leftmostAchievementIndex, rightmostAchievementIndex);
        stepsOffBy = leftmostAchievementIndex - 1;

        //color of icons and text
        if ((step - stepsOffBy) === 1) {
            $('.first-step div').addClass('circle-lg').removeClass('circle-sm');
            $('.first-step span').addClass('text-lg').removeClass('text-sm');
            $('.first-step h5').addClass('heading-lg')
                .removeClass('heading-sm');
        }
        if ((step - stepsOffBy) === 2) {
            $('.second-step div').addClass('circle-lg')
                .removeClass('circle-sm');
            $('.second-step span').addClass('text-lg')
                .removeClass('text-sm');
            $('.second-step h5').addClass('heading-lg')
                .removeClass('heading-sm');
        }
        if ((step - stepsOffBy) === 3) {
            $('.third-step div').addClass('circle-lg')
                .removeClass('circle-sm');
            $('.third-step span').addClass('text-lg')
                .removeClass('text-sm');
            $('.third-step h5').addClass('heading-lg')
                .removeClass('heading-sm');
        }
        if ((step - stepsOffBy) === 4) {
            $('.fourth-step div').addClass('circle-lg')
                .removeClass('circle-sm');
            $('.fourth-step span').addClass('text-lg')
                .removeClass('text-sm');
            $('.fourth-step h5').addClass('heading-lg')
                .removeClass('heading-sm');
        }
        if ((step - stepsOffBy) === 5) {
            $('.fifth-step div').addClass('circle-lg')
                .removeClass('circle-sm');
            $('.fifth-step span').addClass('text-lg')
                .removeClass('text-sm');
            $('.fifth-step h5').addClass('heading-lg')
                .removeClass('heading-sm');
        }
    });

    // When profile picture for username is not found, show a dummy image
    $(".profile_picture").on("error", function () {
        $(this).attr('src', '/outreachy-wikicv/static/user_summary/' +
                'img/dummy.jpg');
    });

    // Handle badges
    var imgSrc = "";
    if (badges.special_rights_badge) {
        $('.rights-badge .badge').text(badges.special_rights_badge[0]);
        $('.rights-badge .badge').addClass('badge-' +
                badges.special_rights_badge[1]);
        imgSrc = badgeMedalImageSource(badges.special_rights_badge[1]);
        $('.rights-badge img').attr('src', imgSrc);
    } else {
        $('.rights-badge').addClass('hidden');
    }

    if (badges.bytes_added_badge) {
        $('.bytes-badge .badge').text(badges.bytes_added_badge[0]);
        $('.bytes-badge .badge').addClass('badge-' +
                badges.bytes_added_badge[1]);
        imgSrc = badgeMedalImageSource(badges.bytes_added_badge[1]);
        $('.bytes-badge img').attr('src', imgSrc);
    } else {
        $('.bytes-badge').addClass('hidden');
    }

    if (badges.year_badge) {
        $('.years-badge .badge').text(badges.year_badge[0]);
        $('.years-badge .badge').addClass('badge-' + badges.year_badge[1]);
        imgSrc = badgeMedalImageSource(badges.year_badge[1]);
        $('.years-badge img').attr('src', imgSrc);
    } else {
        $('.years-badge').addClass('hidden');
    }

});
