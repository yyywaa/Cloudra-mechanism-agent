import { expect, test } from '@playwright/test';
import { installApiMocks, openSpa } from './fixtures';

test('folder picker localizes failures, retries and selection', async ({ page }) => {
  await installApiMocks(page, { projects: [], jobs: [] });
  let attempts = 0;
  await page.route('**/api/v2/fs/browse*', async (route) => {
    attempts += 1;
    if (attempts === 1) return route.fulfill({ status: 401, json: { detail: 'invalid token' } });
    return route.fulfill({ json: { current: '/work', parent: '/', home: '/home', cwd: '/work', writable: true, shortcuts: [], entries: [{ name: 'reactions', path: '/work/reactions', is_dir: true }] } });
  });
  await openSpa(page);
  await page.getByRole('button', { name: '选择项目', exact: true }).click();
  await page.getByRole('button', { name: '新建项目', exact: true }).click();
  await page.getByRole('dialog', { name: '新建项目', exact: true }).getByRole('button', { name: '选择', exact: true }).click();
  const picker = page.getByRole('dialog', { name: '选择文件夹', exact: true });
  await expect(picker.getByRole('alert')).toContainText('登录状态已失效');
  await expect(picker.getByText('此文件夹中没有子文件夹', { exact: true })).toHaveCount(0);
  await expect(picker.getByRole('button', { name: '选择', exact: true })).toBeDisabled();
  await expect(picker.getByText('GUI Picker', { exact: true })).toHaveCount(0);
  await picker.getByRole('button', { name: '重试', exact: true }).click();
  await picker.getByRole('button', { name: 'reactions', exact: true }).click();
  await picker.getByRole('button', { name: '选择', exact: true }).click();
  await expect(page.getByRole('dialog', { name: '新建项目', exact: true }).getByLabel('文件夹', { exact: true })).toHaveValue('/work/reactions');
  await page.getByRole('dialog', { name: '新建项目', exact: true }).getByRole('button', { name: '取消', exact: true }).click();
  await page.getByRole('button', { name: '设置', exact: true }).click();
  await page.getByLabel('语言', { exact: true }).selectOption('en');
  await page.getByRole('button', { name: 'Back to chat', exact: true }).click();
  await page.getByRole('button', { name: 'Choose project', exact: true }).click();
  await page.getByRole('button', { name: 'New project', exact: true }).click();
  await page.getByRole('dialog', { name: 'New project', exact: true }).getByRole('button', { name: 'Choose', exact: true }).click();
  await expect(page.getByRole('dialog', { name: 'Choose folder', exact: true }).getByRole('button', { name: 'Select', exact: true })).toBeEnabled();
  await expect(page.getByLabel('Folder path', { exact: true })).toBeVisible();
});

test('composer model menu searches models and saves reasoning without settings navigation', async ({ page }) => {
  await installApiMocks(page, { projects: [], jobs: [] });
  const slot = { provider: 'example', model: 'model-a', url: 'https://example.test/v1', key_set: true, context_window: 1000, timeout: 60, reasoning_effort: 'medium' };
  const config = { config_file: '/test/config.yaml', coordinator: { ...slot }, follower: { ...slot } };
  const patches: Array<{ slot: string; changes: Record<string, unknown> }> = [];
  await page.route('**/api/v2/runtime/config', async (route) => {
    if (route.request().method() === 'PATCH') {
      const patch = route.request().postDataJSON(); patches.push(patch);
      Object.assign(config.coordinator, patch.changes);
    }
    return route.fulfill({ json: config });
  });
  await page.route('**/api/v2/runtime/providers', (route) => route.fulfill({ json: [{ id: 'example', name: 'Example', default_model: 'model-a', default_url: slot.url, models: ['model-a', 'model-b'], context_window: 1000, supports_vision: true, native_search: '' }] }));
  await openSpa(page);
  await page.getByRole('button', { name: '选择模型', exact: true }).click();
  const menu = page.getByRole('dialog', { name: '模型选择', exact: true });
  await expect(menu.getByRole('heading', { name: 'Example', exact: true })).toBeVisible();
  await expect(menu.getByRole('button', { name: 'model-a', exact: true })).toHaveAttribute('aria-pressed', 'true');
  await menu.getByRole('button', { name: '高', exact: true }).click();
  await expect.poll(() => patches.length).toBe(1);
  expect(patches[0]).toEqual({ slot: 'coordinator', changes: { model: 'model-a', reasoning_effort: 'high' } });
  await menu.getByLabel('搜索模型', { exact: true }).fill('model-b');
  await expect(menu.getByRole('button', { name: 'model-a', exact: true })).toHaveCount(0);
  await menu.getByRole('button', { name: 'model-b', exact: true }).click();
  await expect(page.getByRole('button', { name: '选择模型', exact: true })).toContainText('model-b');
  await page.getByRole('button', { name: '设置', exact: true }).click();
  await expect(page.getByRole('navigation', { name: '设置分类', exact: true }).getByRole('button', { name: '模型', exact: true })).toHaveCount(0);
});
