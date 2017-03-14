module.exports = {
    "env": {
        "browser": true,
        "jquery": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "addLoadEvent": true,
        "connect": true,
        "doXHR": true,
        "evalJSON": true,
        "forEach": true,
        "getElementsByTagAndClassName": true,
        "hasElementClass": true,
        "hideElement": true,
        "log": true,
        "removeElementClass": true,
        "showElement": true
    },
    "rules": {
        "indent": [
            "error",
            4
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "no-unused-vars": [
            "error",
            {"vars": "all", "args": "none"}
        ],
        "quotes": [
            "error",
            "single"
        ],
        "semi": [
            "error",
            "always"
        ]
    }
};
