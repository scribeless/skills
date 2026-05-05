import { execFileSync, spawnSync } from 'node:child_process'
import { existsSync, mkdtempSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { basename, join, relative } from 'node:path'

const root = new URL('..', import.meta.url).pathname
const skillsDir = join(root, 'skills')
const pluginPath = join(root, '.codex-plugin', 'plugin.json')
const namePattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/
const forbiddenPatterns = [
  /\/Users\//,
  /(?:^|[/\\])\.env(?:$|\b)/,
  /access[_ -]?token/i,
  /bearer\s+[a-z0-9._-]+/i,
  /Linear/i,
  /Intercom/i,
]

let failures = 0

function fail(message) {
  failures += 1
  console.error(`FAIL ${message}`)
}

function pass(message) {
  console.log(`OK ${message}`)
}

function readSkillFrontmatter(skillPath) {
  const content = readFileSync(join(skillPath, 'SKILL.md'), 'utf8')
  const match = content.match(/^---\n([\s\S]*?)\n---\n/)
  if (!match) return { content, frontmatter: null }
  const frontmatter = Object.fromEntries(
    match[1]
      .split('\n')
      .map((line) => line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/))
      .filter(Boolean)
      .map((m) => [m[1], m[2].replace(/^"|"$/g, '')]),
  )
  return { content, frontmatter }
}

function scanForForbiddenContent(filePath) {
  const text = readFileSync(filePath, 'utf8')
  for (const pattern of forbiddenPatterns) {
    if (pattern.test(text)) fail(`${relative(root, filePath)} contains forbidden internal content: ${pattern}`)
  }
}

function walkFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name)
    if (entry.isDirectory()) return walkFiles(path)
    return [path]
  })
}

if (!existsSync(skillsDir)) fail('skills directory is missing')
if (!existsSync(pluginPath)) fail('.codex-plugin/plugin.json is missing')

const plugin = JSON.parse(readFileSync(pluginPath, 'utf8'))
if (plugin.name !== 'scribeless') fail('plugin name must be scribeless')
if (plugin.skills !== './skills/') fail('plugin skills path must be ./skills/')
if ((plugin.interface?.defaultPrompt ?? []).length > 3) fail('plugin defaultPrompt must have at most 3 entries')
pass('plugin manifest parsed')

const skillNames = readdirSync(skillsDir, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort()

if (skillNames.length !== 5) fail(`expected 5 skills, found ${skillNames.length}`)

for (const skillName of skillNames) {
  const skillPath = join(skillsDir, skillName)
  const skillFile = join(skillPath, 'SKILL.md')
  if (!existsSync(skillFile)) {
    fail(`${skillName} is missing SKILL.md`)
    continue
  }

  if (!namePattern.test(skillName)) fail(`${skillName} is not kebab-case`)

  const { content, frontmatter } = readSkillFrontmatter(skillPath)
  if (!frontmatter) {
    fail(`${skillName} has no YAML frontmatter`)
  } else {
    if (frontmatter.name !== skillName) fail(`${skillName} frontmatter name does not match folder`)
    if (!frontmatter.description || frontmatter.description.length < 80) {
      fail(`${skillName} description should be specific enough for discovery`)
    }
  }

  if (content.length > 20000) fail(`${skillName} SKILL.md is too large`)

  const openaiYaml = join(skillPath, 'agents', 'openai.yaml')
  if (!existsSync(openaiYaml)) {
    fail(`${skillName} missing agents/openai.yaml`)
  } else {
    const yaml = readFileSync(openaiYaml, 'utf8')
    if (!yaml.includes(`$${skillName}`)) fail(`${skillName} openai.yaml default prompt must mention $${skillName}`)
  }

  for (const file of walkFiles(skillPath)) {
    if (statSync(file).isFile() && /\.(md|ya?ml|json|csv|py|js|mjs)$/.test(file)) {
      scanForForbiddenContent(file)
    }
  }

  pass(`${skillName} metadata validated`)
}

const recipientSkill = join(skillsDir, 'scribeless-recipient-data-prep')
const fixture = join(recipientSkill, 'fixtures', 'valid-recipients.csv')
const invalidFixture = join(recipientSkill, 'fixtures', 'invalid-recipients.csv')
const validateScript = join(recipientSkill, 'scripts', 'validate_recipients.py')
const payloadScript = join(recipientSkill, 'scripts', 'build_recipient_payload.py')

if (existsSync(validateScript) && existsSync(payloadScript)) {
  const temp = mkdtempSync(join(tmpdir(), 'scribeless-skills-'))
  const reportPath = join(temp, 'report.json')
  const payloadPath = join(temp, 'payload.json')
  execFileSync('python3', [validateScript, fixture, '--report', reportPath], { stdio: 'inherit' })
  const invalidResult = spawnSync('python3', [validateScript, invalidFixture], { stdio: 'inherit' })
  if (invalidResult.status === 0) fail('invalid recipient fixture should fail validation')
  execFileSync('python3', [payloadScript, fixture, '--campaign-id', 'CAMPAIGN_ID', '--output', payloadPath], { stdio: 'inherit' })
  const payload = JSON.parse(readFileSync(payloadPath, 'utf8'))
  if (payload.campaignId !== 'CAMPAIGN_ID') fail('payload campaignId mismatch')
  if (!Array.isArray(payload.data) || payload.data.length !== 2) fail('payload data should contain 2 recipients')
  writeFileSync(join(temp, 'validated'), 'ok')
  pass('recipient helper scripts validated')
} else {
  fail('recipient helper scripts missing')
}

if (failures > 0) {
  console.error(`\n${failures} validation failure(s)`)
  process.exit(1)
}

console.log('\nAll Scribeless skills validated')
