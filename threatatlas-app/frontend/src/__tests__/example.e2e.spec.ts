import { test, expect } from '@playwright/test';

test('homepage smoke', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/ThreatAtlas|Threat/);
  await expect(page.locator('text=Login')).toBeVisible({ timeout: 10000 });
});
