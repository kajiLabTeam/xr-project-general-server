export const getCredential = (authorization: string): string => {
  const authParts = authorization.split(' ');

  if (authParts.length !== 2 || authParts[0].toLowerCase() !== 'basic') {
    throw new Error('Invalid authorization header');
  }

  const decodedBytes = Buffer.from(authParts[1], 'base64');
  const credentials = decodedBytes.toString('utf-8').split(':', 2);

  if (credentials.length !== 2) {
    throw new Error('Invalid credentials format');
  }

  const [appId, secretKey] = credentials;

  return appId;
};
