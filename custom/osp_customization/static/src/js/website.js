$(document).ready(function(){
    if ($('a.s_website_form_send_osp').length) {
        $('#opportunity5').on('focusout change', function (){
            if (this.value) {
                $(document.getElementById('opportunity4')).val(this.value);
            }
        });
    }

    $('#tel_input').click(function(){
         var _divs_intlTelInput = $('.iti.iti--allow-dropdown.iti--separate-dial-code');
        // Ensure there is more than 1
          if (_divs_intlTelInput.length > 1)
          _divs_intlTelInput.first().replaceWith(_divs_intlTelInput.last());
    });


    //Function for industry
    $("#industry").each(function () {

        // Cache the number of options
        var $this = $(this),
            numberOfOptions = $(this).children('option').length;

        // Hides the select element
        $this.addClass('s-hidden');

        // Wrap the select element in a div
        $this.wrap('<div class="select_industry" id="select_industry"></div>');


        var _divs = $('.select_industry');
        // Ensure there is more than 1
          if (_divs.length > 1)
          _divs.first().replaceWith(_divs.last());


        // Insert a styled div to sit over the top of the hidden select element
        $this.after('<div class="styledSelect"></div>');

        // Cache the styled div
        var $styledSelect = $this.next('div.styledSelect');

        // Show the first select option in the styled div
        var styledSelect = $styledSelect.text($this.children('option').eq(0).text());

        // Insert an unordered list after the styled div and also cache the list
        var $list = $('<ul />', {
            'class': 'options industry-scrollable-dropdown'
        }).insertAfter($styledSelect);

        // Insert a list item into the unordered list for each select option
        for (var i = 1; i < numberOfOptions; i++) {
            $('<li />', {
                text: $this.children('option').eq(i).text(),
                rel: $this.children('option').eq(i).val()
            }).appendTo($list);
        }

        // Cache the list items
        var $listItems = $list.children('li');

        // Show the unordered list when the styled div is clicked (also hides it if the div is clicked again)
        $styledSelect.click(function (e) {
            e.stopPropagation();
            $('div.styledSelect.active').each(function () {
                $(this).removeClass('active').next('ul.options').hide();
            });
            $(this).toggleClass('active').next('ul.options').toggle();
        });

        // Hides the unordered list when a list item is clicked and updates the styled div to show the selected list item
        // Updates the select element to have the value of the equivalent option
        $listItems.click(function (e) {
            e.stopPropagation();
            $styledSelect.text($(this).text()).removeClass('active');
            $this.val($(this).attr('rel'));
            $list.hide();
            // Other industry always have id=1,
            // as its loaded from the data file when module installed &
            // can not be deleted
            if ($this.val() == 1) {
                $('.other_industry_div').removeClass('d-none');
                $('#other_industry').prop('required', true);
            } else {
                $('.other_industry_div').addClass('d-none');
                $('#other_industry').prop('required', false);
            }
            /* alert($this.val()); Uncomment this for demonstration! */
        });

        // Hides the unordered list when clicking outside of it
        $(document).click(function () {
            $styledSelect.removeClass('active');
            $list.hide();
        });

    });

    //Function for annual revenue
    $("#annual_revenue").each(function () {

        // Cache the number of options
        var $this = $(this),
            numberOfOptions = $(this).children('option').length;

        // Hides the select element
        $this.addClass('s-hidden');

        // Wrap the select element in a div
        $this.wrap('<div class="select_annual_range" id="select"></div>');

       var divs_annual = $('.select_annual_range');
        // Ensure there is more than 1
          if (divs_annual.length > 1)
          divs_annual.first().replaceWith(divs_annual.last());

        // Insert a styled div to sit over the top of the hidden select element
        $this.after('<div class="styledSelect"></div>');

        // Cache the styled div
        var $styledSelect = $this.next('div.styledSelect');

        // Show the first select option in the styled div
        var styledSelect = $styledSelect.text($this.children('option').eq(0).text());

        // Insert an unordered list after the styled div and also cache the list
        var $list = $('<ul />', {
            'class': 'options'
        }).insertAfter($styledSelect);

        // Insert a list item into the unordered list for each select option
        for (var i = 1; i < numberOfOptions; i++) {
            $('<li />', {
                text: $this.children('option').eq(i).text(),
                rel: $this.children('option').eq(i).val()
            }).appendTo($list);
        }

        // Cache the list items
        var $listItems = $list.children('li');

        // Show the unordered list when the styled div is clicked (also hides it if the div is clicked again)
        $styledSelect.click(function (e) {
            e.stopPropagation();
            $('div.styledSelect.active').each(function () {
                $(this).removeClass('active').next('ul.options').hide();
            });
            $(this).toggleClass('active').next('ul.options').toggle();
        });

        // Hides the unordered list when a list item is clicked and updates the styled div to show the selected list item
        // Updates the select element to have the value of the equivalent option
        $listItems.click(function (e) {
            e.stopPropagation();
            $styledSelect.text($(this).text()).removeClass('active');
            $this.val($(this).attr('rel'));
            $list.hide();
            /* alert($this.val()); Uncomment this for demonstration! */
        });

        // Hides the unordered list when clicking outside of it
        $(document).click(function () {
            $styledSelect.removeClass('active');
            $list.hide();
        });

    });

    //Function for employee range
    $("#solution_type").each(function () {

        // Cache the number of options
        var $this = $(this),
            numberOfOptions = $(this).children('option').length;

        // Hides the select element
        $this.addClass('s-hidden');

        // Wrap the select element in a div
        $this.wrap('<div class="select_solution" id="select"></div>');

        var divs_solution = $('.select_solution');
        // Ensure there is more than 1
          if (divs_solution.length > 1)
          divs_solution.first().replaceWith(divs_solution.last());

        // Insert a styled div to sit over the top of the hidden select element
        $this.after('<div class="styledSelect"></div>');

        // Cache the styled div
        var $styledSelect = $this.next('div.styledSelect');

        // Show the first select option in the styled div
        var styledSelect = $styledSelect.text($this.children('option').eq(0).text());

        // Insert an unordered list after the styled div and also cache the list
        var $list = $('<ul />', {
            'class': 'options'
        }).insertAfter($styledSelect);

        // Insert a list item into the unordered list for each select option
        for (var i = 1; i < numberOfOptions; i++) {
            $('<li />', {
                text: $this.children('option').eq(i).text(),
                rel: $this.children('option').eq(i).val()
            }).appendTo($list);
        }

        // Cache the list items
        var $listItems = $list.children('li');

        // Show the unordered list when the styled div is clicked (also hides it if the div is clicked again)
        $styledSelect.click(function (e) {
            e.stopPropagation();
            $('div.styledSelect.active').each(function () {
                $(this).removeClass('active').next('ul.options').hide();
            });
            $(this).toggleClass('active').next('ul.options').toggle();
        });

        // Hides the unordered list when a list item is clicked and updates the styled div to show the selected list item
        // Updates the select element to have the value of the equivalent option
        $listItems.click(function (e) {
            e.stopPropagation();
            $styledSelect.text($(this).text()).removeClass('active');
            $this.val($(this).attr('rel'));
            $list.hide();
            /* alert($this.val()); Uncomment this for demonstration! */
        });

        // Hides the unordered list when clicking outside of it
        $(document).click(function () {
            $styledSelect.removeClass('active');
            $list.hide();
        });

    });

    //Function for employee range
    $("#timeline").each(function () {

        // Cache the number of options
        var $this = $(this),
            numberOfOptions = $(this).children('option').length;

        // Hides the select element
        $this.addClass('s-hidden');

        // Wrap the select element in a div
        $this.wrap('<div class="select_timeline" id="select"></div>');

        var divs_timeline = $('.select_timeline');
        // Ensure there is more than 1
          if (divs_timeline.length > 1)
          divs_timeline.first().replaceWith(divs_timeline.last());

        // Insert a styled div to sit over the top of the hidden select element
        $this.after('<div class="styledSelect"></div>');

        // Cache the styled div
        var $styledSelect = $this.next('div.styledSelect');

        // Show the first select option in the styled div
        var styledSelect = $styledSelect.text($this.children('option').eq(0).text());

        // Insert an unordered list after the styled div and also cache the list
        var $list = $('<ul />', {
            'class': 'options'
        }).insertAfter($styledSelect);

        // Insert a list item into the unordered list for each select option
        for (var i = 1; i < numberOfOptions; i++) {
            $('<li />', {
                text: $this.children('option').eq(i).text(),
                rel: $this.children('option').eq(i).val()
            }).appendTo($list);
        }

        // Cache the list items
        var $listItems = $list.children('li');

        // Show the unordered list when the styled div is clicked (also hides it if the div is clicked again)
        $styledSelect.click(function (e) {
            e.stopPropagation();
            $('div.styledSelect.active').each(function () {
                $(this).removeClass('active').next('ul.options').hide();
            });
            $(this).toggleClass('active').next('ul.options').toggle();
        });

        // Hides the unordered list when a list item is clicked and updates the styled div to show the selected list item
        // Updates the select element to have the value of the equivalent option
        $listItems.click(function (e) {
            e.stopPropagation();
            $styledSelect.text($(this).text()).removeClass('active');
            $this.val($(this).attr('rel'));
            $list.hide();
            /* alert($this.val()); Uncomment this for demonstration! */
        });

        // Hides the unordered list when clicking outside of it
        $(document).click(function () {
            $styledSelect.removeClass('active');
            $list.hide();
        });

    });

    //Click submit button verify is all fields been fill up
    $('#submit_button').click(function(e) {

        $("#submit_invalid").hide();
        //Check Customer Category is selected or not
        document.getElementById("category_error").innerHTML = "Required.";
        var category_radios = document.getElementsByName('category');
        $("#category_error").show();
        var category_error = true;
        for (var i = 0, length = category_radios.length; i < length; i++) {
            if (category_radios[i].checked) {
                $("#category_error").hide();
                category_error = false;
                break;
            }
        }

        //Check preferred module must choose at least one
        document.getElementById("module_error").innerHTML = "Required. Please select at least one.";
        preferred_module =  $("input[name='preferred_module']:checked").length;
            if(!preferred_module) {
            $("#module_error").show();
            }
            else {
            $("#module_error").hide();
            }

        //Check Industry is selected or not
        document.getElementById("industry_error").innerHTML = "Required.";
        document.getElementById("other_industry_error").innerHTML = "Required.";
        var industry_val = document.getElementById('industry');
        if(industry_val.value == 0) {
            $("#industry_error").show();
        } else if (industry_val.value == '1' && !document.getElementById('other_industry').value) {
            $("#other_industry_error").show();
        } else {
            $("#industry_error").hide();
            $("#other_industry_error").hide();
        }

        //Check Customer Business modal is selected or not
        document.getElementById("business_modal_error").innerHTML = "Required.";
        var business_modal_radios = document.getElementsByName('business_modal');
        $("#business_modal_error").show();
        var business_modal_error = true;
        for (var i = 0, length = business_modal_radios.length; i < length; i++) {
            if (business_modal_radios[i].checked) {
                $("#business_modal_error").hide();
                business_modal_error = false;
                break;
            }
        }

        //Check First Time User is selected or not
        document.getElementById("first_time_error").innerHTML = "Required.";
        var first_time_user_radios = document.getElementsByName('first_time_user');
        $("#first_time_error").show();
        var first_time_error = true;
        for (var i = 0, length = first_time_user_radios.length; i < length; i++) {
            if (first_time_user_radios[i].checked) {
                $("#first_time_error").hide();
                first_time_error = false;
                break;
            }
        }

        //Check Annual Revenue is selected or not
        document.getElementById("annual_error").innerHTML = "Required.";
            if(document.getElementById('annual_revenue').value == 0) {
            $("#annual_error").show();
            }
            else {
            $("#annual_error").hide();
            }

        //Check Solution Needed is selected or not
        document.getElementById("solution_error").innerHTML = "Required.";
            if(document.getElementById('solution_type').value == 0) {
            $("#solution_error").show();
            }
            else {
            $("#solution_error").hide();
            }

        // Check timeline been selected or not
        document.getElementById("timeline_error").innerHTML = "Required.";
            if(document.getElementById('timeline').value == 0) {
            $("#timeline_error").show();
                }
            else {
            $("#timeline_error").hide();
            }

        //Check is company been fill up or not
       document.getElementById("company_error").innerHTML = "Required.";
            if(document.getElementById('name').value == 0) {
            $("#company_error").show();
                }
            else {
            $("#company_error").hide();
            }

            //Check customer job role fill up or not
            document.getElementById("job_role_error").innerHTML = "Required.";
            if(document.getElementById('function').value == 0) {
                $("#job_role_error").show();
            }
            else {
                $("#job_role_error").hide();
            }

        //Check customer requirement fill up or not
    //    var customer_requirement = document.getElementById("requirement_error").innerHTML = "Required.";
    //        if(document.getElementById('customer_requirement').value == 0) {
    //            $("#requirement_error").show();
    //            }
    //        else {
    //            $("#requirement_error").hide();
    //        }

        //Check customer name fill up or not
        document.getElementById("name_error").innerHTML = "Required.";
            if(document.getElementById('contact_name').value == 0) {
            $("#name_error").show();
            }
            else {
            $("#name_error").hide();
            }

        //Check job Role fill up or not
    //    var job = document.getElementById("function_error").innerHTML = "Required.";
    //        if(document.getElementById('function').value == 0) {
    //            $("#function_error").show();
    //            }
    //        else {
    //            $("#function_error").hide();
    //        }

        //Check phone number fill up or not
        var phone = document.getElementById("phone_error").innerHTML = "Required.";
            if((document.getElementById('phone').value == 0)) {
                $("#phone_error").show();
                $('input.intlTelInput').addClass('is-invalid');
                }
            else {
                $("#phone_error").hide();
                $('input.intlTelInput').removeClass('is-invalid');
            }

        //Check phone number valid or not
    //    var phone_invalid = document.getElementById("phone_invalid").innerHTML = "Please enter a valid phone number.";
        document.getElementById("phone_invalid").innerHTML = "Please enter a valid phone number.";
        var phoneField = $("input#phone")
        var phoneformat = new RegExp ("^([+]([-]?[0-9]){7,16}|([-]?[0-9]){7,16})$")
            if(!phoneformat.test(phoneField.val())) {
                $("#phone_invalid").show();
                $('input.intlTelInput').addClass('is-invalid');
                }
            else {
                $("#phone_invalid").hide();
                $('input.intlTelInput').removeClass('is-invalid');
            }

        //Check email fill up or not
        var email = document.getElementById("email_error").innerHTML = "Required.";
            if(document.getElementById('email_from').value == 0) {
                $("#email_error").show();
                $('input.emailInput').addClass('is-invalid');
                }
            else {
                $("#email_error").hide();
                $('input.emailInput').removeClass('is-invalid');
            }

        //Check Email format
        document.getElementById("email_invalid").innerHTML = "Please enter a valid email.";
        var emailField = $("input[type=email]");
        var mailformat = new RegExp("^(([^<>()[\\]\\\\.,;:\\s@\"]+(\\.[^<>()[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$");
            if (!mailformat.test(emailField.val())) {
                $("#email_invalid").show();
                emailField.addClass('is-invalid');
                return false;
            } else {
                $("#email_invalid").hide();
                emailField.removeClass('is-invalid');
            }

        if((!preferred_module)||(document.getElementById('industry').value == 0)||
            (document.getElementById('industry').value == '1' && !document.getElementById('other_industry').value)||
            (document.getElementById('timeline').value == 0)||(first_time_error)||
            (document.getElementById('function').value == 0)||(category_error)||(business_modal_error)||
            (document.getElementById('solution_type').value == 0)||(document.getElementById('annual_revenue').value == 0)||
            (document.getElementById('name').value == 0)||(document.getElementById('contact_name').value == 0)||
            (document.getElementById('email_from').value == 0)||(!phoneformat.test(phoneField.val()))||
            (document.getElementById('phone').value == 0)||(!mailformat.test(emailField.val()))){
            return false;
        }

    });

});
