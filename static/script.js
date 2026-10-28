let systemCallChart = null;
let faultChart = null;


async function runAnalysis() {

    const program =
        document.getElementById("program").value;

    const status =
        document.getElementById("status");

    status.innerText =
        "Running analysis... Please wait.";

    try {

        const response =
            await fetch("/run", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    program: program
                })

            });


        const result =
            await response.json();


        if (!result.success) {

            status.innerText =
                "Error: " + result.message;

            return;
        }


        status.innerText =
            "Analysis completed successfully.";

        await updateDashboard();


    } catch (error) {

        status.innerText =
            "Error connecting to server.";

        console.error(error);

    }

}


async function updateDashboard() {

    const response =
        await fetch("/api/analysis");

    const data =
        await response.json();


    document.getElementById("totalCalls")
        .innerText =
        data.total_system_calls;


    document.getElementById("successfulCalls")
        .innerText =
        data.successful_calls;


    document.getElementById("totalFaults")
        .innerText =
        data.total_faults;


    updateSystemCallChart(data);

    updateFaultChart(data);


    // System call table

    const systemTable =
        document.getElementById(
            "systemCallTable"
        );

    systemTable.innerHTML = "";


    for (const [syscall, count]
        of Object.entries(
            data.system_call_frequency
        )) {

        const row =
            document.createElement("tr");


        row.innerHTML =
            `<td>${syscall}</td>
             <td>${count}</td>`;


        systemTable.appendChild(row);

    }


    // Fault table

    const faultTable =
        document.getElementById(
            "faultTable"
        );

    faultTable.innerHTML = "";


    for (const [error, count]
        of Object.entries(
            data.fault_frequency
        )) {

        const row =
            document.createElement("tr");


        row.className =
            "fault-row";


        row.innerHTML =
            `<td>${error}</td>
             <td>${count}</td>`;


        faultTable.appendChild(row);

    }


    // Fault details

    const faultDetails =
        document.getElementById(
            "faultDetails"
        );

    faultDetails.innerHTML = "";


    for (const fault
        of data.faults) {

        const div =
            document.createElement("div");


        div.className =
            "fault";


            div.innerHTML =
            `<h3>
                ${fault.error} -
                ${fault.description}
             </h3>
        
             <p>
                <strong>System Call:</strong>
                ${fault.syscall}
             </p>
        
             <p>
                <strong>Category:</strong>
                ${fault.category}
             </p>
        
             <p>
                <strong>Severity:</strong>
                ${fault.severity}
             </p>
        
             <p>
                <strong>Recommended Action:</strong>
                ${fault.recommended_action}
             </p>
        
             <p>
                <strong>Trace Line:</strong>
                ${fault.line}
             </p>
        
             <p class="trace">
                ${fault.trace}
             </p>`;


        faultDetails.appendChild(div);

    }

}


/* -------------------------------- */
/* SYSTEM CALL BAR CHART            */
/* -------------------------------- */

function updateSystemCallChart(data) {

    const container =
        document.getElementById(
            "systemCallChart"
        );


    container.innerHTML = "";


    const calls =
        Object.entries(
            data.system_call_frequency
        );


    calls.sort(
        (a, b) => b[1] - a[1]
    );


    const maxValue =
        calls.length > 0
            ? calls[0][1]
            : 1;


    for (const [name, count]
        of calls) {

        const row =
            document.createElement("div");


        row.className =
            "chart-row";


        const label =
            document.createElement("div");


        label.className =
            "chart-label";


        label.innerText =
            name;


        const barContainer =
            document.createElement("div");


        barContainer.className =
            "bar-container";


        const bar =
            document.createElement("div");


        bar.className =
            "bar";


        const width =
            (count / maxValue) * 100;


        bar.style.width =
            width + "%";


        const value =
            document.createElement("span");


        value.className =
            "bar-value";


        value.innerText =
            count;


        barContainer.appendChild(bar);

        barContainer.appendChild(value);

        row.appendChild(label);

        row.appendChild(barContainer);

        container.appendChild(row);

    }

}


/* -------------------------------- */
/* FAULT BAR CHART                  */
/* -------------------------------- */

function updateFaultChart(data) {

    const container =
        document.getElementById(
            "faultChart"
        );


    container.innerHTML = "";


    const faults =
        Object.entries(
            data.fault_frequency
        );


    if (faults.length === 0) {

        container.innerHTML =
            "<p class='success'>No faults detected.</p>";

        return;

    }


    const maxValue =
        Math.max(
            ...faults.map(
                item => item[1]
            ),
            1
        );


    for (const [name, count]
        of faults) {

        const row =
            document.createElement("div");


        row.className =
            "chart-row";


        const label =
            document.createElement("div");


        label.className =
            "chart-label";


        label.innerText =
            name;


        const barContainer =
            document.createElement("div");


        barContainer.className =
            "bar-container";


        const bar =
            document.createElement("div");


        bar.className =
            "fault-bar";


        const width =
            (count / maxValue) * 100;


        bar.style.width =
            width + "%";


        const value =
            document.createElement("span");


        value.className =
            "bar-value";


        value.innerText =
            count;


        barContainer.appendChild(bar);

        barContainer.appendChild(value);

        row.appendChild(label);

        row.appendChild(barContainer);

        container.appendChild(row);

    }

}