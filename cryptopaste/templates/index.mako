<%inherit file="base.mako"/>
<%block name="robots">index, follow</%block>
<%block name="title">Add a new paste</%block>
<%block name="head">
    <script src="${request.static_url('cryptopaste:static/form.min.js')}"></script>
</%block>

<form method="post">
    <div id="tools">
        <button class="send right" type="submit">Send</button>
        <div class="button">
            <label for="expiration">
                <span>Expiration</span>
                <select id="expiration" name="expiration">
                    <option value="0.001">1 minute</option>
                    <option value="0.003">5 minutes</option>
                    <option value="0.007">10 minutes</option>
                    <option value="0.010">15 minutes</option>
                    <option value="0.021">30 minutes</option>
                    <option value="0.042">1 hour</option>
                    <option value="0.5">12 hours</option>
                    <option value="1">24 hours</option>
                    <option value="7">1 week</option>
                    <option value="30.417">1 month</option>
                    <option value="3650">1 year</option>
                    <option value="36500" selected>100 years</option>
                    <option value="365000">1 000 years</option> <!-- One day -->
                </select>
            </label>
        </div>
        &nbsp;
        <div class="button">
            <label for="burn">
                <span>Burn after reading</span>
                <input class="w" id="burn" name="burn" type="checkbox" onchange="p()">
            </label>
        </div>
    </div>

    <div id="fields">
        <label for="user">
            <span class="b">Nickname for the paste (optional)</span>
            <input
                    type="text" id="user" name="user" placeholder="Optional and must only contain alphanumerics characters." pattern="^[a-zA-Z0-9]{1,80}$"
                    % if 'user' in request.POST:
                        value="${user}"
                    % endif
            />
        </label>

        <label for="encryption" title="If the encryption is asked, a key will be required to read it (can be set below, or automatically generated).">
            <span>To be encrypted (AES256)</span>
            <input type="checkbox" id="encryption" name="encryption" class="w" checked onchange="o()"/>
        </label>

        <label for="area">
            <span class="b">Paste content</span>
            <textarea id="area" name="content" placeholder="Paste content" required rows="27">${content}</textarea>
        </label>

        <label for="key" class="key" title="The Decryption Key to decrypt (and encrypt) the paste content if the encryption is asked.
Remember: the decryption key will be asked to display the paste.">
            <span class="b"><a href="#">[Help]</a> Decryption key (optional)</span>
            <input type="text" id="key" name="key" placeholder="Optional and automatically generated if blank. Must only contain alphanumerics characters and the following characters -._" pattern="^[a-zA-Z0-9\-._]{1,500}$" />
        </label>
    </div>
</form>

<script>o();p()</script>