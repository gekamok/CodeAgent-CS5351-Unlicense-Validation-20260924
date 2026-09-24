import assert from 'node:assert/strict';
import test from 'node:test';

import { JavaScriptChecker } from '../../../skills/CodeAgent/scripts/codeagent_js_checker.js';

function checkerWithAvailableAnalyzers() {
    const checker = new JavaScriptChecker();
    checker.eslintAvailable = true;
    checker.tscAvailable = true;
    checker._runESLint = () => ({ available: true, issues: [], error: null });
    checker._runTypeScript = () => ({ available: true, issues: [], error: null });
    return checker;
}

test('accepts safe JavaScript and reports a safe risk level', () => {
    const result = checkerWithAvailableAnalyzers().check('const message = "hello";');

    assert.equal(result.passed, true);
    assert.equal(result.security.risk_level, 'safe');
    assert.equal(result.issues.some((issue) => issue.tool === 'security'), false);
});

test('reports direct eval as a critical security issue', () => {
    const result = checkerWithAvailableAnalyzers().check('function run(input) { return eval(input); }');

    assert.equal(result.passed, false);
    assert.equal(result.security.risk_level, 'critical');
    assert.equal(result.issues.some((issue) => issue.tool === 'security' && issue.level === 'critical'), true);
});

test('resets findings between checks on the same checker instance', () => {
    const checker = checkerWithAvailableAnalyzers();
    checker.check('eval("unsafe");');

    const result = checker.check('const message = "safe";');

    assert.equal(result.passed, true);
    assert.equal(result.security.risk_level, 'safe');
    assert.equal(result.issues.some((issue) => issue.tool === 'security'), false);
});

test('locates the Node executable using the platform command locator', () => {
    assert.equal(new JavaScriptChecker()._checkCommand('node'), true);
});

test('allocates a separate temporary workspace per checker run', () => {
    const first = new JavaScriptChecker();
    const second = new JavaScriptChecker();

    try {
        first._setupTempDir('const first = 1;', 'javascript');
        second._setupTempDir('const second = 2;', 'javascript');

        assert.notEqual(first.tempDir, second.tempDir);
    } finally {
        first._cleanup();
        second._cleanup();
    }
});

test('does not report a pass when a requested analysis tool is unavailable', () => {
    const checker = new JavaScriptChecker();
    checker.eslintAvailable = false;
    checker.tscAvailable = false;

    const result = checker.check('const value: string = "typed";', '', 'typescript');

    assert.equal(result.passed, false);
    assert.match(result.summary, /检查未完成/);
    assert.match(result.summary, /ESLint/);
    assert.match(result.summary, /TypeScript/);
});
