import security from 'eslint-plugin-security';
import globals from 'globals';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import js from '@eslint/js';
import { FlatCompat } from '@eslint/eslintrc';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all
});

export default [...compat.extends('eslint:recommended'),
    security.configs.recommended,
    {
        plugins: {
            security,
        },

        languageOptions: {
            globals: {
                ...globals.browser,
                ...globals.jquery,
                addLoadEvent: true,
                connect: true,
                doXHR: true,
                evalJSON: true,
                forEach: true,
                getElementsByTagAndClassName: true,
                hasElementClass: true,
                hideElement: true,
                log: true,
                removeElementClass: true,
                showElement: true,
                getFirstParentByTagAndClassName: true,
                getFirstElementByTagAndClassName: true,
                Draggable: true,
                bind: true,
                getElementPosition: true,
                getElement: true,
                getElementDimensions: true,
                addElementClass: true,
                removeElement: true,
                disconnectAll: true,
                DIV: true,
                appendChildNodes: true,
                setStyle: true,
                partial: true,
                replaceChildNodes: true,
                OPTION: true,
                getStyle: true,
                TD: true,
                IMG: true,
                OpenLayers: true,
                TR: true,
                insertSiblingNodesBefore: true,
                google: true,
                STATIC_URL: true,
                MochiKit: true,
            },
        },

        rules: {
            indent: ['error', 4],
            'linebreak-style': ['error', 'unix'],

            'no-unused-vars': ['error', {
                vars: 'all',
                args: 'none',
            }],

            quotes: ['error', 'single'],
            semi: ['error', 'always'],

            'max-len': [2, {
                code: 80,
                tabWidth: 4,
                ignoreUrls: true,
            }],

            'space-before-function-paren': ['error', 'never'],
            'space-in-parens': ['error', 'never'],
            'no-trailing-spaces': ['error'],

            'key-spacing': ['error', {
                beforeColon: false,
            }],

            'func-call-spacing': ['error', 'never'],

            'keyword-spacing': ['error', {
                before: true,
                after: true,
            }],

            'brace-style': ['error', '1tbs'],
            'security/detect-buffer-noassert': 1,
            'security/detect-child-process': 1,
            'security/detect-disable-mustache-escape': 1,
            'security/detect-eval-with-expression': 1,
            'security/detect-new-buffer': 1,
            'security/detect-no-csrf-before-method-override': 1,
            'security/detect-non-literal-fs-filename': 1,
            'security/detect-non-literal-regexp': 1,
            'security/detect-non-literal-require': 0,
            'security/detect-object-injection': 0,
            'security/detect-possible-timing-attacks': 1,
            'security/detect-pseudoRandomBytes': 1,
            'security/detect-unsafe-regex': 1,
        },
    }];