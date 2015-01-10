## -*- coding: utf-8 -*-
<!doctype HTML>

<html>
    <head>
        <title><%block name="title" /> | CryptoPaste</title>
        <meta name="robots" content="<%block name="robots">noindex, nofollow</%block>">
        <meta name="viewport" content="width=device-width, initial-scape=1" />
        <meta name="description" content="<%block name='description' />" />
        <link rel="stylesheet" type="text/css" href="${request.static_url('cryptopaste:static/style.min.css')}" />
        <%block name="head" />
    </head>
<body>
    <header>
        <div class="title">
            <a href="${request.route_path('home')}">
                <img src="${request.static_url('cryptopaste:static/logo_little.png')}" alt="logo" />
            </a>
        </div>
        <%block name="menu" />
    </header>

% for f in request.session.pop_flash():
    % if f[0] == 'info':
        <div class="notify info">
            % if f[2] == 'html':
                ${f[1]|n}
            % else:
                ${f[1]}
            % endif
        </div>

    % elif f[0] == 'warn':
        <div class="notify warning">
            Warning:
            % if f[2] == 'html':
                ${f[1]|n}
            % else:
                ${f[1]}
            % endif
        </div>

    % else:
        <div class="notify error">
            Error:
            % if f[2] == 'html':
                ${f[1]|n}
            % else:
                ${f[1]}
            % endif
        </div>
    % endif
% endfor

            <section>
${self.body()}
            </section>
        <footer class="footer right">
                CryptoPaste - Paste with an AES encryption and Python while keeping the quickness and privacy.
        </footer>
    </body>
</html>
