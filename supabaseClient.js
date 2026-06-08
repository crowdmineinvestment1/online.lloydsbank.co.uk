// supabaseClient.js – initialize Supabase client
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm';

const SUPABASE_URL = 'https://ursrbmvgrpjhuogfimal.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_tPbGnhGMinGYFI5tc4KbvA_7Gu2Ketw';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
