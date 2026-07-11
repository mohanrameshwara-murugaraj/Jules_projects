import { test, expect } from '@playwright/test';

test('redirects to login', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1').first()).toHaveText('Sign in to AI Coach');
});