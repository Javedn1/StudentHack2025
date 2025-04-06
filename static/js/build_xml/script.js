document.addEventListener('DOMContentLoaded', function () {
    let webformCount = 1;
    let testCount = 1;
    let stepCount = 1;

    // Add Field functionality
    document.getElementById('add-field-btn-1').addEventListener('click', function () {
        const fieldSection = document.createElement('div');
        fieldSection.classList.add('field-section');
        fieldSection.innerHTML = `
            <input type="text" placeholder="Field ID" class="field-id">
            <input type="text" placeholder="Field Name" class="field-name">
            <input type="text" placeholder="Field Type" class="field-type">
            <button type="button" class="remove-field-btn">Remove Field</button>
        `;
        document.querySelector('#webform-1 .fieldset-section').appendChild(fieldSection);

        // Remove Field functionality
        fieldSection.querySelector('.remove-field-btn').addEventListener('click', function () {
            fieldSection.remove();
        });
    });

    // Add Test functionality
    document.getElementById('add-test-btn-1').addEventListener('click', function () {
        const testSection = document.createElement('div');
        testSection.classList.add('test-section');
        testSection.innerHTML = `
            <label for="test-description-${testCount}">Test Description</label>
            <input type="text" id="test-description-${testCount}" placeholder="Enter test description">
            <label for="test-language-${testCount}">Test Language</label>
            <input type="text" id="test-language-${testCount}" value="en" placeholder="Enter language">

            <div class="steps-section" id="steps-${testCount}">
                <h4>Steps</h4>
                <div class="step-section" id="step-${stepCount}">
                    <input type="text" placeholder="Step Access By" class="step-accessby">
                    <input type="text" placeholder="Step Key" class="step-key">
                    <input type="text" placeholder="Step Value" class="step-value">
                    <button type="button" class="remove-step-btn">Remove Step</button>
                </div>
                <button type="button" id="add-step-btn-${stepCount}">Add Step</button>
            </div>
            <button type="button" class="remove-test-btn">Remove Test</button>
        `;
        document.querySelector('#webform-1 .tests-section').appendChild(testSection);

        // Remove Test functionality
        testSection.querySelector('.remove-test-btn').addEventListener('click', function () {
            testSection.remove();
        });

        // Add Step functionality
        testSection.querySelector(`#add-step-btn-${stepCount}`).addEventListener('click', function () {
            const stepSection = document.createElement('div');
            stepSection.classList.add('step-section');
            stepSection.innerHTML = `
                <input type="text" placeholder="Step Access By" class="step-accessby">
                <input type="text" placeholder="Step Key" class="step-key">
                <input type="text" placeholder="Step Value" class="step-value">
                <button type="button" class="remove-step-btn">Remove Step</button>
            `;
            document.querySelector(`#steps-${testCount}`).appendChild(stepSection);

            // Remove Step functionality
            stepSection.querySelector('.remove-step-btn').addEventListener('click', function () {
                stepSection.remove();
            });
        });

        testCount++;
        stepCount++;
    });

    // Generate XML
    document.getElementById('generate-xml-btn').addEventListener('click', function (e) {
        e.preventDefault();

        const version = document.getElementById('version').value;
        const useragents = document.getElementById('useragents').value.split(',');

        let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
        xml += `<!-- Generated XML Configuration -->\n`;
        xml += `<!DOCTYPE generic-web-testing SYSTEM "web-testing.dtd">\n`;
        xml += `<generic-web-testing version="${version}">\n`;

        xml += `<webforms useragents="${useragents.join(',')}">\n`;

        // Handle Webform
        document.querySelectorAll('.webform').forEach(function (webform, index) {
            const url = webform.querySelector(`#url-${index + 1}`).value;
            const formid = webform.querySelector(`#formid-${index + 1}`).value;
            const timeout = webform.querySelector(`#timeout-${index + 1}`).value;
            const submissiontimeout = webform.querySelector(`#submissiontimeout-${index + 1}`).value;

            xml += `  <webform url="${url}" formid="${formid}" timeout="${timeout}" submissiontimeout="${submissiontimeout}">\n`;

            // Handle Fields
            xml += `    <fieldset>\n`;
            webform.querySelectorAll('.field-section').forEach(function (fieldSection) {
                const id = fieldSection.querySelector('.field-id').value;
                const name = fieldSection.querySelector('.field-name').value;
                const type = fieldSection.querySelector('.field-type').value;
                xml += `      <field id="${id}" name="${name}" type="${type}"></field>\n`;
            });
            xml += `    </fieldset>\n`;

            // Handle Tests
            xml += `    <tests>\n`;
            webform.querySelectorAll('.test-section').forEach(function (testSection) {
                const description = testSection.querySelector('input[id^="test-description"]').value;
                const language = testSection.querySelector('input[id^="test-language"]').value;

                xml += `      <test id="${index + 1}" description="${description}" run="true" language="${language}">\n`;

                // Handle Steps
                xml += `        <steps>\n`;
                testSection.querySelectorAll('.step-section').forEach(function (stepSection) {
                    const accessby = stepSection.querySelector('.step-accessby').value;
                    const key = stepSection.querySelector('.step-key').value;
                    const value = stepSection.querySelector('.step-value').value;
                    xml += `          <step accessby="${accessby}" key="${key}" value="${value}" />\n`;
                });
                xml += `        </steps>\n`;

                xml += `      </test>\n`;
            });
            xml += `    </tests>\n`;
            xml += `  </webform>\n`;
        });

        xml += `</webforms>\n`;
        xml += `</generic-web-testing>\n`;

        // Display generated XML
        document.getElementById('generated-xml').textContent = xml;
    });

    // Handle download functionality
    document.getElementById('download-xml-btn').addEventListener('click', function () {
        const xml = document.getElementById('generated-xml').textContent;
        const blob = new Blob([xml], { type: 'application/xml' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'generated-config.xml';
        link.click();
    });
});