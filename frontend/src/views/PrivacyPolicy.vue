<template>
  <div class="privacy-policy">
    <el-container>
      <el-main>
        <div class="privacy-content">
          <div class="content-section">
            <h1>{{ $t('privacy.title') }}</h1>
            <p class="last-updated">{{ $t('privacy.lastUpdated', { date: lastUpdated }) }}</p>

            <h2>1. {{ $t('privacy.sections.introduction') }}</h2>
            <p v-if="$i18n.locale === 'en'">Welcome to Avatar Replacement Online ("we," "our," or "us"). This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website and use our avatar replacement service.</p>
            <p v-else>欢迎使用头像替换在线服务（"我们"或"本服务"）。本隐私政策说明了当您访问我们的网站并使用我们的头像替换服务时，我们如何收集、使用、披露和保护您的信息。</p>

            <h2>2. {{ $t('privacy.sections.informationCollection') }}</h2>
            <h3>2.1 {{ $t('privacy.sections.informationProvided') }}</h3>
            <ul v-if="$i18n.locale === 'en'">
              <li>Images you upload for avatar replacement processing</li>
              <li>Session data during your use of the service</li>
            </ul>
            <ul v-else>
              <li>您上传用于头像替换处理的图片</li>
              <li>您使用服务期间的会话数据</li>
            </ul>

            <h3>2.2 {{ $t('privacy.sections.automaticCollection') }}</h3>
            <ul v-if="$i18n.locale === 'en'">
              <li>IP address and browser information</li>
              <li>Usage data and analytics through third-party services</li>
              <li>Cookies and similar tracking technologies</li>
            </ul>
            <ul v-else>
              <li>IP地址和浏览器信息</li>
              <li>通过第三方服务收集的使用数据和分析</li>
              <li>Cookies和类似的跟踪技术</li>
            </ul>

            <h2>3. {{ $t('privacy.sections.informationUse') }}</h2>
            <p v-if="$i18n.locale === 'en'">We use the collected information to:</p>
            <p v-else>我们使用收集的信息来：</p>
            <ul v-if="$i18n.locale === 'en'">
              <li>Provide and maintain our avatar replacement service</li>
              <li>Process and analyze uploaded images</li>
              <li>Improve our website and service functionality</li>
              <li>Communicate with you about our service</li>
              <li>Ensure security and prevent fraud</li>
            </ul>
            <ul v-else>
              <li>提供和维护我们的头像替换服务</li>
              <li>处理和分析上传的图片</li>
              <li>改进我们的网站和服务功能</li>
              <li>与您就我们的服务进行沟通</li>
              <li>确保安全并防止欺诈</li>
            </ul>

            <h2>4. {{ $t('privacy.sections.dataStorage') }}</h2>
            <ul v-if="$i18n.locale === 'en'">
              <li>Uploaded images are temporarily stored for processing and automatically deleted after session completion</li>
              <li>We implement appropriate security measures to protect your data</li>
              <li>Session data is automatically cleaned up according to our retention policy</li>
            </ul>
            <ul v-else>
              <li>上传的图片临时存储用于处理，会话完成后自动删除</li>
              <li>我们实施适当的安全措施来保护您的数据</li>
              <li>会话数据根据我们的保留政策自动清理</li>
            </ul>

            <h2>5. {{ $t('privacy.sections.thirdPartyServices') }}</h2>
            <p v-if="$i18n.locale === 'en'">Our website may use third-party services including:</p>
            <p v-else>我们的网站可能使用第三方服务，包括：</p>
            <ul v-if="$i18n.locale === 'en'">
              <li>Google AdSense for advertising</li>
              <li>Analytics services to understand website usage</li>
              <li>Content delivery networks (CDN) for performance</li>
            </ul>
            <ul v-else>
              <li>Google AdSense用于广告投放</li>
              <li>分析服务来了解网站使用情况</li>
              <li>内容分发网络（CDN）以提升性能</li>
            </ul>

            <h2>6. {{ $t('privacy.sections.cookiesTracking') }}</h2>
            <p v-if="$i18n.locale === 'en'">We use cookies and similar technologies to:</p>
            <p v-else>我们使用cookies和类似技术来：</p>
            <ul v-if="$i18n.locale === 'en'">
              <li>Maintain your session preferences</li>
              <li>Analyze website traffic and usage patterns</li>
              <li>Provide personalized advertising through Google AdSense</li>
            </ul>
            <ul v-else>
              <li>维护您的会话偏好设置</li>
              <li>分析网站流量和使用模式</li>
              <li>通过Google AdSense提供个性化广告</li>
            </ul>

            <h2>7. {{ $t('privacy.sections.userRights') }}</h2>
            <p v-if="$i18n.locale === 'en'">You have the right to:</p>
            <p v-else>您有权：</p>
            <ul v-if="$i18n.locale === 'en'">
              <li>Access and request deletion of your personal data</li>
              <li>Opt-out of data collection where applicable</li>
              <li>Disable cookies through your browser settings</li>
            </ul>
            <ul v-else>
              <li>访问和请求删除您的个人数据</li>
              <li>在适用情况下选择退出数据收集</li>
              <li>通过浏览器设置禁用cookies</li>
            </ul>

            <h2>8. {{ $t('privacy.sections.childrenPrivacy') }}</h2>
            <p v-if="$i18n.locale === 'en'">Our service is not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13.</p>
            <p v-else>我们的服务不适用于13岁以下的儿童。我们不会故意收集13岁以下儿童的个人信息。</p>

            <h2>9. {{ $t('privacy.sections.policyChanges') }}</h2>
            <p v-if="$i18n.locale === 'en'">We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date.</p>
            <p v-else>我们可能会不时更新本隐私政策。我们将通过在本页面发布新的隐私政策并更新"最后更新时间"来通知您任何变更。</p>

            <h2>10. {{ $t('privacy.sections.contactUs') }}</h2>
            <p v-if="$i18n.locale === 'en'">If you have any questions about this Privacy Policy, please contact us through our website.</p>
            <p v-else>如果您对本隐私政策有任何疑问，请通过我们的网站联系我们。</p>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

export default {
  name: 'PrivacyPolicy',
  setup() {
    const { t } = useI18n()
    const lastUpdated = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })

    return {
      lastUpdated
    }
  }
}
</script>

<style scoped>
.privacy-policy {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px 0;
}

.privacy-content {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.content-section h1 {
  color: #409eff;
  text-align: center;
  margin-bottom: 10px;
  font-size: 2.5em;
  font-weight: 600;
}

.last-updated {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e6e6e6;
}

.content-section h2 {
  color: #333;
  margin-top: 30px;
  margin-bottom: 15px;
  font-size: 1.4em;
  font-weight: 600;
  border-left: 4px solid #409eff;
  padding-left: 15px;
}

.content-section h3 {
  color: #555;
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 1.1em;
  font-weight: 500;
}

.content-section p {
  line-height: 1.6;
  margin-bottom: 15px;
  color: #333;
  text-align: justify;
}

.content-section ul {
  margin: 15px 0;
  padding-left: 30px;
}

.content-section li {
  line-height: 1.6;
  margin-bottom: 8px;
  color: #333;
}

@media (max-width: 768px) {
  .privacy-content {
    margin: 0 10px;
    padding: 20px;
  }

  .content-section h1 {
    font-size: 2em;
  }

  .content-section h2 {
    font-size: 1.2em;
  }
}
</style>