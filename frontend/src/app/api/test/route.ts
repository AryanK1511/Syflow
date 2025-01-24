import { getAccessToken, withApiAuthRequired } from '@auth0/nextjs-auth0';

import type { NextApiRequest, NextApiResponse } from 'next';

export const GET = withApiAuthRequired(async (req: NextApiRequest, res: NextApiResponse) => {
    try {
        // Get the access token
        const { accessToken } = await getAccessToken(req, res);

        // Fetch data from the external API
        const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/auth/private`, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });

        // Handle the response from the external API
        if (!response.ok) {
            throw new Error(`Failed to fetch products: ${response.statusText}`);
        }

        const products = await response.json();

        // Return the products as a JSON response
        return new Response(JSON.stringify(products), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (error) {
        console.error('Error fetching products:', error);

        // Return an error response
        return new Response(JSON.stringify({ error: 'Failed to fetch products' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
        });
    }
});
