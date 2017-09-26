$(document).ready(function () {
    // From https://github.com/twitter/typeahead.js/blob/master/doc/bloodhound.md
    // WARNING: While it's possible to get away with it for smaller data sets, prefetched data isn't meant
    // to contain entire sets of data. Rather, it should act as a first-level cache. Ignoring this warning
    // means you'll run the risk of hitting local storage limits.
    var interests = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: 'static/data/interests.json',
            cacheKey: 'interests', // Key that data will be stored in local storage under. Defaults to value of url.
            ttl: 300,              // 5 minutes (vs the default of 1 day)
        }
    });

    var locations = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: 'static/data/locations.json',
            cacheKey: 'locations', // Key that data will be stored in local storage under. Defaults to value of url.
            ttl: 300,              // 5 minutes (vs the default of 1 day)
        },
    });

    function interestsWithDefaults(q, sync) {
        if (q === '') {
            //  console.log(interests.get('Nature', 'People', 'Animals')); // Should return ["Nature"]
            sync(interests.get('Nature', 'People', 'Animals'));
        } else {
            interests.search(q, sync);
        }
    }

    function locationsWithDefaults(q, sync) {
        if (q === '') {
            //  console.log(locations.get('Wellington', 'ChristChurch', 'Auckland')); // Should return ["Wellington"]
            sync(locations.get('Wellington', 'ChristChurch', 'Auckland'));
        } else {
            locations.search(q, sync);
        }
    }

    $('#interests .typeahead').typeahead({
            minLength: 0,
            highlight: true,
            limit: 20

        },
        {
            name: 'interests',
            source: interestsWithDefaults
        });

    $('#locations .typeahead').typeahead({
            minLength: 0,
            highlight: true,
        },
        {
            name: 'locations',
            limit: 20,
            source: locationsWithDefaults
        });


    $('#submit').on('click', function (e) {
        console.log("Someone submitted somethning");
        var interestsInput = $("#interestsInput").val();
        var locationInput = $("#locationInput").val();

        console.log("interest input is: " + interestsInput);
        console.log("location input is" + locationInput);

        target = '/results/' + "notUsedYet" + '/' + locationInput + '/' + interestsInput
        location.href = target;
        return false;
    });
});