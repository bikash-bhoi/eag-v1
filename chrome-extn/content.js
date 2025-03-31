// Helper functions for generating random data
function getRandomFirstName() {
    const firstNames = [
        "Aarav", "Advait", "Arjun", "Vihaan", "Reyansh", "Aanya", "Saanvi", "Aadhya", "Ishaan", "Kabir",
        "Priya", "Neha", "Rahul", "Amit", "Sneha", "Kavya", "Arun", "Riya", "Rohan", "Meera",
        "Dev", "Zara", "Aryan", "Diya", "Vivaan", "Ananya", "Aditi", "Arnav", "Avni", "Krish"
    ];
    return firstNames[Math.floor(Math.random() * firstNames.length)];
}

function getRandomLastName() {
    const lastNames = [
        "Sharma", "Patel", "Kumar", "Singh", "Verma", "Gupta", "Malhotra", "Reddy", "Kapoor", "Joshi",
        "Mehta", "Shah", "Chopra", "Bansal", "Sinha", "Rao", "Desai", "Iyer", "Nair", "Menon"
    ];
    return lastNames[Math.floor(Math.random() * lastNames.length)];
}

function getRandomName() {
    return `${getRandomFirstName()} ${getRandomLastName()}`;
}

function getRandomEmail(name) {
    const domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"];
    const randomName = name.toLowerCase().replace(" ", ".") + Math.floor(Math.random() * 1000);
    return `${randomName}@${domains[Math.floor(Math.random() * domains.length)]}`;
}

function getRandomPassword() {
    return Math.random().toString(36).slice(-10) + Math.floor(Math.random() * 10) + "Aa!";
}

// Define PIN code ranges for states
const STATE_PINCODES = {
    "Delhi": {
        ranges: [
            [110001, 110096], // New Delhi
            [110100, 110124]  // Delhi NCR
        ]
    },
    "Maharashtra": {
        ranges: [
            [400001, 400107], // Mumbai
            [411001, 411062], // Pune
            [440001, 440037], // Nagpur
            [422001, 422013], // Nashik
            [401101, 401107]  // Thane
        ]
    },
    "Karnataka": {
        ranges: [
            [560001, 560103], // Bangalore
            [570001, 570029], // Mysore
            [580001, 580033], // Hubli
            [575001, 575017]  // Mangalore
        ]
    },
    "Tamil Nadu": {
        ranges: [
            [600001, 600119], // Chennai
            [641001, 641047], // Coimbatore
            [625001, 625020], // Madurai
            [636001, 636016]  // Salem
        ]
    },
    "Gujarat": {
        ranges: [
            [380001, 380063], // Ahmedabad
            [395001, 395017], // Surat
            [390001, 390023], // Vadodara
            [360001, 360007]  // Rajkot
        ]
    },
    "Telangana": {
        ranges: [
            [500001, 500095], // Hyderabad
            [501101, 501512], // Hyderabad Rural
            [502001, 502371], // Medak
            [503001, 503307]  // Nizamabad
        ]
    },
    "West Bengal": {
        ranges: [
            [700001, 700157], // Kolkata
            [711101, 711414], // Howrah
            [713101, 713419], // Hooghly
            [721101, 721668]  // Midnapore
        ]
    },
    "Uttar Pradesh": {
        ranges: [
            [226001, 226031], // Lucknow
            [208001, 208027], // Kanpur
            [201001, 201017], // Noida
            [201301, 201310]  // Greater Noida
        ]
    }
};

function getRandomPinCodeForState(state) {
    if (!STATE_PINCODES[state]) {
        // Fallback if state not found
        return "110001";
    }

    // Get random range for the state
    const ranges = STATE_PINCODES[state].ranges;
    const selectedRange = ranges[Math.floor(Math.random() * ranges.length)];

    // Generate random PIN within the selected range
    const [min, max] = selectedRange;
    return String(Math.floor(Math.random() * (max - min + 1) + min));
}

function getRandomIndianAddress() {
    // Building types
    const buildingTypes = [
        "Apartment", "Heights", "Towers", "Residency", "Complex",
        "Plaza", "Arcade", "Mansion", "House", "Villa"
    ];

    // Society names
    const societyNames = [
        "Green Valley", "Sun City", "Royal Palm", "Lake View",
        "Golden Park", "Silver Oak", "River Side", "Mountain View",
        "Peace Haven", "Garden City", "Shanti Niwas", "Krishna Gardens",
        "Gokul Heights", "Sai Enclave", "Ganesh Colony"
    ];

    // Street types
    const streetTypes = [
        "Main Road", "Cross", "Layout", "Street", "Avenue",
        "Circle", "Highway", "Lane", "Path", "Marg",
        "Nagar", "Colony", "Society", "Extension", "Sector"
    ];

    // Landmarks
    const landmarks = [
        "Near Railway Station", "Opposite Bus Stop", "Near Metro Station",
        "Behind City Mall", "Near Government Hospital", "Opposite Post Office",
        "Near Police Station", "Next to Park", "Near School", "Near Temple",
        "Near Market", "Opposite Bank", "Behind Municipal Office",
        "Near Shopping Complex", "Next to College"
    ];

    // Select random state and city
    const state = Object.keys(STATE_PINCODES)[Math.floor(Math.random() * Object.keys(STATE_PINCODES).length)];
    const cityData = STATE_PINCODES[state];

    // Get cities based on PIN code ranges
    const cities = {
        "Delhi": ["New Delhi", "Delhi"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane"],
        "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
        "Telangana": ["Hyderabad", "Secunderabad"],
        "West Bengal": ["Kolkata", "Howrah"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Noida", "Greater Noida"]
    };

    const city = cities[state][Math.floor(Math.random() * cities[state].length)];

    // Generate building/flat details
    const flatNumber = Math.floor(Math.random() * 999) + 1;
    const buildingType = buildingTypes[Math.floor(Math.random() * buildingTypes.length)];
    const societyName = societyNames[Math.floor(Math.random() * societyNames.length)];

    // Generate street details
    const streetNumber = Math.floor(Math.random() * 100) + 1;
    const streetType = streetTypes[Math.floor(Math.random() * streetTypes.length)];

    // Select landmark
    const landmark = landmarks[Math.floor(Math.random() * landmarks.length)];

    // Get PIN code for the selected state
    const pinCode = getRandomPinCodeForState(state);

    // Address formats
    const addressFormats = [
        // Format 1: Flat, Building, Street, Landmark, City, State, PIN
        `Flat ${flatNumber}, ${societyName} ${buildingType}, ${streetNumber} ${streetType}, ${landmark}, ${city}, ${state} - ${pinCode}`,

        // Format 2: Building, Street, Area, City, State, PIN
        `${flatNumber}, ${societyName} ${buildingType}, ${streetNumber} ${streetType}, ${city}, ${state} - ${pinCode}`,

        // Format 3: House number, Street, Landmark, City, State, PIN
        `${flatNumber}, ${streetNumber} ${streetType}, ${landmark}, ${city}, ${state} - ${pinCode}`
    ];

    // Select random format
    const selectedFormat = addressFormats[Math.floor(Math.random() * addressFormats.length)];
    console.log("Generated Address", selectedFormat, city, pinCode, state);
    return [selectedFormat, city, pinCode, state];
}


function getRandomMobileNumber() {
    const prefixes = ["7", "8", "9"];
    return prefixes[Math.floor(Math.random() * prefixes.length)] + Math.random().toString().slice(2, 11);
}

function isAddressField(input) {
    const name = (input.name || "").toLowerCase();
    const id = (input.id || "").toLowerCase();
    const placeholder = (input.placeholder || "").toLowerCase();
    const label = input.labels && input.labels[0] ? input.labels[0].textContent.toLowerCase() : "";

    const addressIndicators = [
        'address', 'street', 'road', 'lane', 'apartment', 'apt',
        'suite', 'unit', 'building', 'floor', 'house',
        'landmark', 'area', 'locality', 'sector', 'block',
        'district', 'region', 'colony', 'society'
    ];

    return addressIndicators.some(indicator =>
        name.includes(indicator) ||
        id.includes(indicator) ||
        placeholder.includes(indicator) ||
        label.includes(indicator)
    );
}

function isOptionalField(input) {
    // Get all text content associated with the field
    const name = (input.name || "").toLowerCase();
    const id = (input.id || "").toLowerCase();
    const placeholder = (input.placeholder || "").toLowerCase();
    const label = input.labels && input.labels[0] ? input.labels[0].textContent.toLowerCase() : "";
    const ariaLabel = (input.getAttribute('aria-label') || "").toLowerCase();

    // Common optional indicators
    const optionalIndicators = [
        'optional',
        '(optional)',
        '[optional]',
        'if any',
        '(if any)',
        'if available',
        '(if available)',
        'not required',
        '(not required)'
    ];

    // Check if field is marked as required
    const isRequired =
        input.required ||
        input.getAttribute('aria-required') === 'true' ||
        input.classList.contains('required') ||
        input.hasAttribute('data-required') ||
        (label && label.includes('*'));

    if (isRequired) {
        return false;
    }

    // Check immediate text content for optional indicators
    const hasOptionalIndicator = optionalIndicators.some(indicator =>
        name.includes(indicator) ||
        id.includes(indicator) ||
        placeholder.includes(indicator) ||
        label.includes(indicator) ||
        ariaLabel.includes(indicator)
    );

    if (hasOptionalIndicator) {
        return true;
    }

    // Check surrounding elements for optional indicators
    let element = input;
    let depth = 0;
    const maxDepth = 3; // Check up to 3 levels up

    while (element && depth < maxDepth) {
        // Check siblings
        const siblings = [...element.parentElement.children];
        for (const sibling of siblings) {
            if (sibling !== element && sibling.textContent) {
                const siblingText = sibling.textContent.toLowerCase();
                if (optionalIndicators.some(indicator => siblingText.includes(indicator))) {
                    return true;
                }
            }
        }

        // Move up to parent
        element = element.parentElement;
        depth++;
    }

    // Special handling for address fields
    if (isAddressField(input)) {
        const addressOptionalFields = [
            'apartment', 'apt', 'suite', 'unit', 'building',
            'floor', 'landmark', 'nearby', 'direction',
            'additional', 'extra', 'other', 'alt', 'secondary'
        ];

        const isOptionalAddressField = addressOptionalFields.some(field =>
            name.includes(field) ||
            id.includes(field) ||
            placeholder.includes(field) ||
            label.includes(field) ||
            ariaLabel.includes(field)
        );

        if (isOptionalAddressField) {
            return true;
        }
    }

    return false;
}

// Add this at the top of your content.js
class AddressInfo {
    constructor() {
        const address = this.generateBaseAddress();
        this.flatNumber = address.flatNumber;
        this.buildingName = address.buildingName;
        this.street = address.street;
        this.landmark = address.landmark;
        this.city = address.city;
        this.state = address.state;
        this.pincode = address.pincode;
        this.fullAddress = address.fullAddress;
    }

    generateBaseAddress() {
        const buildingTypes = [
            "Apartment", "Heights", "Towers", "Residency", "Complex",
            "Plaza", "Arcade", "Mansion", "House", "Villa"
        ];

        const societyNames = [
            "Green Valley", "Sun City", "Royal Palm", "Lake View",
            "Golden Park", "Silver Oak", "River Side", "Mountain View",
            "Peace Haven", "Garden City", "Shanti Niwas", "Krishna Gardens"
        ];

        const streetTypes = [
            "Main Road", "Cross", "Layout", "Street", "Avenue",
            "Circle", "Highway", "Lane", "Path", "Marg"
        ];

        const landmarks = [
            "Near Railway Station", "Opposite Bus Stop", "Near Metro Station",
            "Behind City Mall", "Near Government Hospital", "Opposite Post Office",
            "Near Police Station", "Next to Park", "Near School", "Near Temple"
        ];

        // Select random state and get its cities
        const state = Object.keys(STATE_PINCODES)[Math.floor(Math.random() * Object.keys(STATE_PINCODES).length)];
        const cities = {
            "Delhi": ["New Delhi", "Delhi"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane"],
            "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
            "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
            "Telangana": ["Hyderabad", "Secunderabad"],
            "West Bengal": ["Kolkata", "Howrah"],
            "Uttar Pradesh": ["Lucknow", "Kanpur", "Noida", "Greater Noida"]
        };

        const city = cities[state][Math.floor(Math.random() * cities[state].length)];
        const pincode = getRandomPinCodeForState(state);

        // Generate components
        const flatNumber = Math.floor(Math.random() * 999) + 1;
        const buildingType = buildingTypes[Math.floor(Math.random() * buildingTypes.length)];
        const societyName = societyNames[Math.floor(Math.random() * societyNames.length)];
        const streetNumber = Math.floor(Math.random() * 100) + 1;
        const streetType = streetTypes[Math.floor(Math.random() * streetTypes.length)];
        const landmark = landmarks[Math.floor(Math.random() * landmarks.length)];

        const buildingName = `${societyName} ${buildingType}`;
        const street = `${streetNumber} ${streetType}`;
        const fullAddress = `Flat ${flatNumber}, ${buildingName}, ${street}, ${landmark}, ${city}, ${state} - ${pincode}`;

        return {
            flatNumber,
            buildingName,
            street,
            landmark,
            city,
            state,
            pincode,
            fullAddress
        };
    }

    getAddressComponent(fieldName) {
        const nameL = fieldName.toLowerCase();

        if (nameL.includes('flat') || nameL.includes('house')) return `Flat ${this.flatNumber}`;
        if (nameL.includes('building')) return this.buildingName;
        if (nameL.includes('street') || nameL.includes('road')) return this.street;
        if (nameL.includes('landmark')) return this.landmark;
        if (nameL.includes('city')) return this.city;
        if (nameL.includes('state')) return this.state;
        if (nameL.includes('pin') || nameL.includes('zip') || nameL.includes('postal')) return this.pincode;

        // Return full address for general address fields
        return this.fullAddress;
    }
}

// Main form filling function
function fillForm() {
    const password = getRandomPassword();
    const firstName = getRandomFirstName();
    const lastName = getRandomLastName();
    const addressInfo = new AddressInfo();

    // Get all input and select fields
    const inputs = document.getElementsByTagName('input');

    for (let input of inputs) {
        const type = input.type.toLowerCase();
        const name = (input.name || "").toLowerCase();
        const id = (input.id || "").toLowerCase();
        const placeholder = (input.placeholder || "").toLowerCase();
        const label = input.labels && input.labels[0] ? input.labels[0].textContent.toLowerCase() : "";

        // Skip hidden and submit fields
        if (type === 'hidden' || type === 'submit' || type === 'button') continue;

        // Skip captcha fields
        if (name.includes('captcha') || id.includes('captcha') || placeholder.includes('captcha')) continue;

        // Skip optional fields
        if (isOptionalField(input)) {
            console.log('Skipping optional field:', input);
            continue;
        }

        // Fill based on input type and identifiers
        if (type === 'text' || type === 'input') {
            if (name.includes('first') || id.includes('first')) {
                input.value = firstName;
            }
            else if (name.includes('last') || id.includes('last')) {
                input.value = lastName;
            }
            else if (name.includes('name') && !name.includes('first') && !name.includes('last')) {
                input.value = `${firstName} ${lastName}`;
            }
            else if (name.includes('email') || id.includes('email')) {
                input.value = getRandomEmail(`${firstName}.${lastName}`);
            }
            else if (isAddressField(input)) {
                // Get the appropriate address component based on field name/id
                const fieldIdentifier = name || id || placeholder || label;
                input.value = addressInfo.getAddressComponent(fieldIdentifier);
            }
            else if (name.includes('pin') || id.includes('pin') || name.includes('postal') || id.includes('postal') ||
                name.includes('zip') || id.includes('zip')) {
                input.value = addressInfo.pincode;
            }
            else if (name.includes('city')) {
                input.value = addressInfo.city;
            }
            else if (name.includes('state')) {
                input.value = addressInfo.state;
            }

            else if (name.includes('phone') || id.includes('phone') ||
                name.includes('mobile') || id.includes('mobile')) {
                input.value = getRandomMobileNumber();
            }
        } else if (type === 'password') {
            input.value = password;
        } else if (type === 'email') {
            input.value = getRandomEmail(`${firstName}.${lastName}`);
        } else if (type === 'tel') {
            input.value = getRandomMobileNumber();
        }

        // Trigger change events if value was set
        if (input.value) {
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }

    // Handle select elements for city/state if they exist
    const selects = document.getElementsByTagName('select');
    for (let select of selects) {
        const name = (select.name || "").toLowerCase();
        const id = (select.id || "").toLowerCase();

        if (name.includes('city') || id.includes('city')) {
            selectOptionByText(select, addressInfo.city);
        }
        else if (name.includes('state') || id.includes('state') || name.includes('zone') || id.includes('zone')) {
            selectOptionByText(select, addressInfo.state);
        }
    }
}

// Helper function to select option by text
function selectOptionByText(selectElement, text) {
    for (let option of selectElement.options) {
        if (option.text.includes(text)) {
            option.selected = true;
            selectElement.dispatchEvent(new Event('change', { bubbles: true }));
            break;
        }
    }
}

// Add this new function to clear forms
function clearForm() {
    const inputs = document.getElementsByTagName('input');
    const textareas = document.getElementsByTagName('textarea');
    const selects = document.getElementsByTagName('select');

    // Clear input fields
    for (let input of inputs) {
        const type = input.type.toLowerCase();

        // Skip submit, button, and hidden fields
        if (type === 'submit' || type === 'button' || type === 'hidden') continue;

        // Clear the input value
        input.value = '';

        // Uncheck checkboxes and radio buttons
        if (type === 'checkbox' || type === 'radio') {
            input.checked = false;
        }

        // Trigger change events
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new Event('input', { bubbles: true }));
    }

    // Clear textarea fields
    for (let textarea of textareas) {
        textarea.value = '';
        textarea.dispatchEvent(new Event('change', { bubbles: true }));
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
    }

    // Reset select fields to first option
    for (let select of selects) {
        select.selectedIndex = 0;
        select.dispatchEvent(new Event('change', { bubbles: true }));
    }
}

// Add this new function to handle single field filling
function fillSingleField(element) {
    const type = element.type.toLowerCase();
    const name = (element.name || "").toLowerCase();
    const id = (element.id || "").toLowerCase();
    const placeholder = (element.placeholder || "").toLowerCase();
    const label = element.labels && element.labels[0] ? element.labels[0].textContent.toLowerCase() : "";
    const [address, city, pinCode, state] = getRandomIndianAddress();
    console.log("Filling Single Field", address, city, pinCode, state);
    // Handle different field types
    if (type === 'text' || type === 'input') {
        if (name.includes('first') || id.includes('first') ||
            placeholder.includes('first') || label.includes('first')) {
            element.value = getRandomFirstName();
        }
        else if (name.includes('last') || id.includes('last') ||
            placeholder.includes('last') || label.includes('last')) {
            element.value = getRandomLastName();
        }
        else if (name.includes('name') || id.includes('name')) {
            element.value = getRandomName();
        }
        else if (name.includes('email') || id.includes('email')) {
            element.value = getRandomEmail(getRandomName());
        }
        else if (name.includes('address') || id.includes('address')) {
            element.value = address;
        }
        else if ((name.includes('pin') || id.includes('pin') ||
            name.includes('postalCode') || id.includes('postalCode') ||
            placeholder.includes('pin') || placeholder.includes('postalCode') ||
            name.includes('zip') || id.includes('zip'))) {
            element.value = parseInt(pinCode);
        }
        else if (name.includes('phone') || id.includes('phone') ||
            name.includes('mobile') || id.includes('mobile')) {
            element.value = getRandomMobileNumber();
        }
        else if (name.includes('city') || id.includes('city')) {
            element.value = city;
        }
        else if (name.includes('zone') || id.includes('select')) {
            const stateToCode = {
                "Delhi": "DL",
                "Maharashtra": "MH",
                "Karnataka": "KA",
                "Tamil Nadu": "TN",
                "Gujarat": "GJ",
                "Telangana": "TS",
                "West Bengal": "WB",
                "Uttar Pradesh": "UP"
            };
            console.log("State to Code", stateToCode[state]);
            element.value = stateToCode[state] || state;
        }
    } else if (type === 'password') {
        element.value = getRandomPassword();
    } else if (type === 'email') {
        element.value = getRandomEmail(getRandomName());
    } else if (type === 'tel') {
        element.value = getRandomMobileNumber();
    }

    // Trigger change events
    if (element.value) {
        element.dispatchEvent(new Event('change', { bubbles: true }));
        element.dispatchEvent(new Event('input', { bubbles: true }));
    }
}

// Update the message listener to handle both fill and clear commands
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    try {
        if (request.action === "fillForm") {
            fillForm();
        } else if (request.action === "clearForm") {
            clearForm();
        } else if (request.action === "fillField" && request.targetElementId) {
            const element = document.activeElement;
            if (element && element.tagName === 'INPUT') {
                fillSingleField(element);
            }
        }
        sendResponse({ success: true });
    } catch (error) {
        console.error('Error in content script:', error);
        sendResponse({ success: false, error: error.message });
    }
    return true;
}); 