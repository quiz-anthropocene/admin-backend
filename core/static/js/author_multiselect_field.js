document.addEventListener('DOMContentLoaded', function() {
    /**
     * Multiselect dropdown for the authors search form field
     */

    const FORM_ELEMENT = document.querySelector('#id_authorsss');  // disable
    const FORM_PLACEHOLDER = 'Choisir 1 ou plusieurs auteurs';
    const FILTER_PLACEHOLDER = 'Chercher...';

    const buttonTextAndTitle = function(options, select) {
        if (options.length === 0) {
            return FORM_PLACEHOLDER;
        }
        else if (options.length > 4) {
            return `${options.length} auteurs sélectionnés`;
        }
        else {
            var labels = [];
            options.each(function() {
                if ($(this).attr('label') !== undefined) {
                    labels.push($(this).attr('label'));
                }
                else {
                    labels.push($(this).html());
                }
            });
            return labels.join(', ') + '';
        }
    }

    // only on pages with id_authors
    if (document.body.contains(FORM_ELEMENT)) {
        $('#id_authors').multiselect({
            // height & width
            maxHeight: 400,
            buttonWidth: '100%',
            widthSynchronizationMode: 'always',
            // button
            buttonTextAlignment: 'left',
            buttonText: buttonTextAndTitle,
            buttonTitle: buttonTextAndTitle,
            // filter options
            enableFiltering: true,
            enableCaseInsensitiveFiltering: true,
            filterPlaceholder: FILTER_PLACEHOLDER,
            // reset button
            includeResetOption: true,
            includeResetDivider: true,
            resetText: 'Réinitialiser la sélection',
            // enableResetButton: true,
            // resetButtonText: 'Réinitialiser',
            // ability to select all group's child options in 1 click
            enableClickableOptGroups: true,
            // other
            buttonContainer: '<div id="id_author_multiselect" class="btn-group" />',
            widthSynchronizationMode: 'ifPopupIsSmaller',
            // enableHTML: true,
            // nonSelectedText: `<span class="text-muted">${FORM_PLACEHOLDER}</span>`,
            templates: {
                // fix for Bootstrap5: https://github.com/davidstutz/bootstrap-multiselect/issues/1226
                button: '<button type="button" class="form-select multiselect dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false"><span class="multiselect-selected-text"></span></button>'
            },
        });

        // hack to set the placeholder color to grey when there is no item selected
        const multiselectSelectedText = document.querySelector('#id_author_multiselect .multiselect-selected-text');
        if (multiselectSelectedText.innerText === FORM_PLACEHOLDER) {
            multiselectSelectedText.classList.add('text-muted');
        }
        multiselectSelectedText.addEventListener('DOMSubtreeModified', function () {
            if (this.innerText === FORM_PLACEHOLDER) {
                this.classList.add('text-muted');
            } else {
                this.classList.remove('text-muted');
            }
        })
    }

});
