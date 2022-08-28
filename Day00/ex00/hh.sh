#bin/sh
curl -k -H 'User-Agent: api-test-agent' 'https://api.hh.ru/vacancies?text=data-scientist' | jq '.' > hh.json