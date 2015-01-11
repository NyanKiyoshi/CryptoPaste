<%inherit file="base.mako"/>
<%block name="title">View paste</%block>
<div id="tools">
    <a href="${request.path}|raw" class="button right" type="submit">Raw</a>
</div>
<div class="noCSS">
    <b>
        Warning: your CSS seem doesn't work correctly, please try to fix it. If the content of the "paste" doesn't show
        correctly, please add "|raw" at the end of the URL.
    </b>
</div>
% if paste is not UNDEFINED:
    <%
        from datetime import timedelta
        from cryptopaste.utils import td_to_str
    %>
    <div class="notify warn">

        % if type(expiration_delta) is timedelta:
            This document will expire in
            ${'%(seconds)is %(minutes)im %(hours)ih, %(days)i days, %(months)i months and %(years)i years.' % td_to_str(expiration_delta)}
        % else:
                ${expiration_delta}
        % endif
    </div>
    <div class="pContent">${paste}</div>
% else:
    <div class="pContent">
        ${message}
    </div>
% endif
