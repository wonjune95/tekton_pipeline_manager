package demo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.annotation.web.configurers.CsrfConfigurer;
import org.springframework.security.web.SecurityFilterChain;

// 탐지돼야 하는 경우: 요청 위조를 막는 CSRF 토큰 검사를 끔. 끄는 방법마다 한 줄씩
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain legacy(HttpSecurity http) throws Exception {
        // ruleid: mois-1-11-csrf
        http.csrf().disable();
        return http.build();
    }

    @Bean
    public SecurityFilterChain legacyChained(HttpSecurity http) throws Exception {
        // ruleid: mois-1-11-csrf
        http.authorizeRequests().anyRequest().authenticated().and().csrf().disable().formLogin();
        return http.build();
    }

    @Bean
    public SecurityFilterChain lambda(HttpSecurity http) throws Exception {
        // ruleid: mois-1-11-csrf
        http.csrf(csrf -> csrf.disable());
        return http.build();
    }

    @Bean
    public SecurityFilterChain lambdaParenthesized(HttpSecurity http) throws Exception {
        // ruleid: mois-1-11-csrf
        http.csrf((csrf) -> csrf.disable());
        return http.build();
    }

    @Bean
    public SecurityFilterChain lambdaBlock(HttpSecurity http) throws Exception {
        // ruleid: mois-1-11-csrf
        http.csrf(csrf -> {
            csrf.disable();
        });
        return http.build();
    }

    @Bean
    public SecurityFilterChain methodReference(HttpSecurity http) throws Exception {
        // ruleid: mois-1-11-csrf
        return http.csrf(AbstractHttpConfigurer::disable).build();
    }

    @Bean
    public SecurityFilterChain methodReferenceCsrf(HttpSecurity http) throws Exception {
        // ruleid: mois-1-11-csrf
        return http.csrf(CsrfConfigurer::disable).build();
    }

    @Bean
    public SecurityFilterChain methodReferenceQualified(HttpSecurity http) throws Exception {
        // ruleid: mois-1-11-csrf
        return http.csrf(org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer::disable).build();
    }
}
