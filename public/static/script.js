/* =====================================================
   CREDITFIT 360 - STEP 4
===================================================== */

const currentSavings =
    document.getElementById("currentSavings");

const investments =
    document.getElementById("investments");

const emergencyFund =
    document.getElementById("emergencyFund");

const essentialExpenses =
    document.getElementById("essentialExpenses");

const emergencyMonths =
    document.getElementById("emergencyMonths");

const totalAssets =
    document.getElementById("totalAssets");

const fundStatus =
    document.getElementById("fundStatus");

const reserveLevel =
    document.getElementById("reserveLevel");


/* =====================================================
   EMERGENCY FUND CALCULATION
===================================================== */

function calculateEmergencyFund() {

    const savings =
        Number(currentSavings?.value) || 0;

    const investment =
        Number(investments?.value) || 0;

    const emergency =
        Number(emergencyFund?.value) || 0;

    const expenses =
        Number(essentialExpenses?.value) || 0;


    if (totalAssets) {

        totalAssets.value =
            "₹ " +
            (savings + investment)
                .toLocaleString("en-IN");

    }


    if (expenses > 0) {

        const months =
            emergency / expenses;


        if (emergencyMonths) {

            emergencyMonths.value =
                months.toFixed(1) +
                " Months";

        }


        if (months >= 6) {

            if (fundStatus)
                fundStatus.value = "Excellent";

            if (reserveLevel)
                reserveLevel.value =
                    "Strong Financial Reserve";

        }

        else if (months >= 3) {

            if (fundStatus)
                fundStatus.value = "Good";

            if (reserveLevel)
                reserveLevel.value =
                    "Healthy Financial Reserve";

        }

        else if (months >= 1) {

            if (fundStatus)
                fundStatus.value = "Moderate";

            if (reserveLevel)
                reserveLevel.value =
                    "Low Financial Reserve";

        }

        else {

            if (fundStatus)
                fundStatus.value =
                    "Needs Improvement";

            if (reserveLevel)
                reserveLevel.value =
                    "Low Financial Reserve";
        }

    }

    else {

        if (emergencyMonths)
            emergencyMonths.value = "";

        if (fundStatus)
            fundStatus.value = "";

        if (reserveLevel)
            reserveLevel.value = "";

    }

}


/* =====================================================
   LIVE CALCULATION
===================================================== */

if (currentSavings) {

    currentSavings.addEventListener(
        "input",
        calculateEmergencyFund
    );

}

if (investments) {

    investments.addEventListener(
        "input",
        calculateEmergencyFund
    );

}

if (emergencyFund) {

    emergencyFund.addEventListener(
        "input",
        calculateEmergencyFund
    );

}

if (essentialExpenses) {

    essentialExpenses.addEventListener(
        "input",
        calculateEmergencyFund
    );

}


/* =====================================================
   CALCULATE SCORE
===================================================== */

async function calculateScore() {

    const form =
        document.getElementById(
            "savingsForm"
        );


    if (!form) {

        alert("Savings form not found.");

        return;
    }


    if (!form.checkValidity()) {

        form.reportValidity();

        return;
    }


    const savings =
        Number(currentSavings.value);

    const investment =
        Number(investments.value);

    const emergency =
        Number(emergencyFund.value);

    const expenses =
        Number(essentialExpenses.value);


    if (expenses <= 0) {

        alert(
            "Monthly essential expenses must be greater than 0."
        );

        return;
    }


    if (
        emergency >
        savings + investment
    ) {

        alert(
            "Emergency fund cannot be greater than total savings and investments."
        );

        return;
    }


    /* ===============================================
       TEMPORARY STEP 1-3 DATA
    =============================================== */

    const data = {

        /* STEP 1 */

        age: 28,

        income: 60000,

        employmentYears: 5,


        /* STEP 2 */

        householdExpenses: 25000,

        existingEmi: 15000,

        monthlySavings: 5000,

        monthlyInvestment: 5000,


        /* STEP 3 */

        creditScore: 720,

        creditLimit: 100000,

        creditOutstanding: 45000,

        activeLoans: 2,

        missedPayments: 0,

        creditApplications: 1,


        /* STEP 4 */

        currentSavings: savings,

        investments: investment,

        emergencyFund: emergency,

        essentialExpenses: expenses
    };


    try {

        const response =
            await fetch(
                "/calculate-score",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        const result =
            await response.json();


        if (
            !response.ok ||
            !result.success
        ) {

            alert(
                "Error: " +
                (
                    result.error ||
                    "Unable to calculate score."
                )
            );

            return;
        }


        console.log(
            "CreditFit Result:",
            result
        );


        sessionStorage.setItem(
            "creditFitResult",
            JSON.stringify(result)
        );


        alert(
            "CreditFit Score: " +
            result.score +
            "/100\n\n" +
            "Category: " +
            result.category
        );


        window.location.href =
            "/credit-result";


    }

    catch (error) {

        console.error(error);

        alert(
            "Server connection error.\n\n" +
            "Make sure Flask is running."
        );

    }

}


/* =====================================================
   BACK BUTTON
===================================================== */

function goBack() {

    window.history.back();

}


/* =====================================================
   INITIAL CALCULATION
===================================================== */

calculateEmergencyFund();