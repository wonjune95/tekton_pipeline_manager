package demo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;

// 탐지되면 안 되는 경우: CSRF 토큰 검사를 켜 둔다
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // ok: mois-1-11-csrf — 토큰 저장소만 바꾸고 검사는 유지
        http.csrf(csrf -> csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))
            .authorizeHttpRequests(auth -> auth.anyRequest().authenticated());
        return http.build();
    }

    @Bean
    public SecurityFilterChain apiChain(HttpSecurity http) throws Exception {
        // ok: mois-1-11-csrf — 토큰 없는 API 경로만 예외로 두고, 끄는 것은 CSRF 가 아닌 다른 기능
        http.csrf(csrf -> csrf.ignoringRequestMatchers("/api/webhook/**"))
            .httpBasic(AbstractHttpConfigurer::disable)
            .formLogin(form -> form.disable());
        return http.build();
    }

    @Bean
    public SecurityFilterChain defaults(HttpSecurity http) throws Exception {
        // ok: mois-1-11-csrf — 기본값(켜짐)을 그대로 둔다
        http.authorizeHttpRequests(auth -> auth.anyRequest().authenticated());
        http.logout().disable();
        return http.build();
    }
}
